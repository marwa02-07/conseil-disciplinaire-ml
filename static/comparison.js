const form = document.querySelector('#report-form');
const report = document.querySelector('#report-text');
const button = form.querySelector('button');
const formStatus = document.querySelector('#form-status');
const error = document.querySelector('#form-error');
const bertLevel = document.querySelector('#bert-level');
const bertReason = document.querySelector('#bert-reason');
const mlLevel = document.querySelector('#ml-level');
const probabilityHeading = document.querySelector('#probability-heading');
const probabilities = document.querySelector('#ml-probabilities');
const labels = {1: 'Mineur', 2: 'Modéré', 3: 'Grave'};
const percent = new Intl.NumberFormat('fr-FR', {style: 'percent', maximumFractionDigits: 1});

async function analyze(endpoint, reportText) {
    const response = await fetch(endpoint, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({report_text: reportText}),
    });
    const result = await response.json().catch(() => null);
    if (!response.ok || !result) {
        throw new Error(result?.error || `Le serveur a renvoyé une erreur (HTTP ${response.status}).`);
    }
    return result;
}

function showError(message) {
    error.textContent += (error.textContent ? '\n' : '') + message;
    error.hidden = false;
}

function showBert(result) {
    bertLevel.textContent = labels[result.disciplinary_level];
    bertReason.textContent = result.details.reason;
    bertReason.hidden = false;
}

function showMl(result) {
    mlLevel.textContent = labels[result.disciplinary_level];
    for (const name of Object.values(labels)) {
        const row = document.createElement('div');
        const term = document.createElement('dt');
        const value = document.createElement('dd');
        term.textContent = name;
        value.textContent = percent.format(result.probabilities[name.toLowerCase()]);
        row.append(term, value);
        probabilities.append(row);
    }
    probabilityHeading.hidden = false;
    probabilities.hidden = false;
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = report.value.trim();
    error.hidden = true;
    error.textContent = '';
    report.removeAttribute('aria-invalid');
    if (!text) {
        showError('Saisissez un rapport non vide.');
        report.setAttribute('aria-invalid', 'true');
        report.focus();
        return;
    }

    button.disabled = true;
    formStatus.textContent = 'Analyse en cours…';
    bertLevel.textContent = mlLevel.textContent = 'En cours…';
    bertReason.hidden = probabilityHeading.hidden = probabilities.hidden = true;
    probabilities.replaceChildren();

    const methods = [
        {endpoint: form.dataset.bertUrl, name: 'BERT + mots-clés', level: bertLevel, show: showBert},
        {endpoint: form.dataset.mlUrl, name: 'TF-IDF + régression logistique', level: mlLevel, show: showMl},
    ];
    try {
        await Promise.all(methods.map(async ({endpoint, name, level, show}) => {
            try {
                show(await analyze(endpoint, text));
            } catch (failure) {
                level.textContent = 'Indisponible';
                showError(`${name} · ${failure.message}`);
            }
        }));
    } finally {
        formStatus.textContent = '';
        button.disabled = false;
    }
});
