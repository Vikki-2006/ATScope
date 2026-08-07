/**
 * Modern Enterprise Chart.js Initializer Library
 */

function initSparklineChart(canvasId, dataPoints, color = '#2563EB') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataPoints.map((_, i) => i),
            datasets: [{
                data: dataPoints,
                borderColor: color,
                borderWidth: 2,
                fill: false,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: { enabled: false } },
            scales: { x: { display: false }, y: { display: false } }
        }
    });
}

function initAtsScoreDoughnut(canvasId, score) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const remaining = Math.max(0, 100 - score);
    const scoreColor = score >= 80 ? '#16A34A' : (score >= 60 ? '#EA580C' : '#DC2626');

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['ATS Score', 'Remaining'],
            datasets: [{
                data: [score, remaining],
                backgroundColor: [scoreColor, '#1F2937'],
                borderWidth: 0,
                hoverOffset: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '82%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true }
            }
        }
    });
}

function initResumeScoreRadar(canvasId, scores) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Formatting', 'Readability', 'Keywords', 'Skills', 'Experience', 'Education', 'Projects'],
            datasets: [{
                label: 'Candidate Score Rating',
                data: [
                    scores.formatting || 85,
                    scores.readability || 80,
                    scores.keyword || 75,
                    scores.skill || 90,
                    scores.experience || 85,
                    scores.education || 95,
                    scores.project || 80
                ],
                backgroundColor: 'rgba(37, 99, 235, 0.15)',
                borderColor: '#2563EB',
                pointBackgroundColor: '#3B82F6',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: '#1F2937' },
                    grid: { color: '#1F2937' },
                    pointLabels: { color: '#94A3B8', font: { size: 10, family: 'Inter' } },
                    ticks: { display: false, max: 100 }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function initJobMatchLineChart(canvasId) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Audit 1', 'Audit 2', 'Audit 3', 'Audit 4', 'Audit 5', 'Current'],
            datasets: [
                {
                    label: 'ATS Score Trend',
                    data: [65, 72, 78, 84, 88, 92],
                    borderColor: '#2563EB',
                    backgroundColor: 'rgba(37, 99, 235, 0.08)',
                    fill: true,
                    tension: 0.35,
                    borderWidth: 2
                },
                {
                    label: 'Job Match %',
                    data: [55, 68, 70, 79, 82, 86],
                    borderColor: '#16A34A',
                    backgroundColor: 'transparent',
                    borderDash: [4, 4],
                    tension: 0.35,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true, position: 'top', labels: { color: '#94A3B8', font: { size: 11, family: 'Inter' } } }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#1F2937' },
                    ticks: { color: '#94A3B8', font: { size: 10 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94A3B8', font: { size: 10 } }
                }
            }
        }
    });
}

function initScoreHorizontalBar(canvasId, scores) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Formatting', 'Readability', 'Keywords', 'Skills', 'Experience', 'Education', 'Projects'],
            datasets: [{
                data: [
                    scores.formatting || 85,
                    scores.readability || 80,
                    scores.keyword || 75,
                    scores.skill || 90,
                    scores.experience || 85,
                    scores.education || 95,
                    scores.project || 80
                ],
                backgroundColor: '#2563EB',
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#1F2937' },
                    ticks: { color: '#94A3B8', font: { size: 10 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#94A3B8', font: { size: 10 } }
                }
            }
        }
    });
}
