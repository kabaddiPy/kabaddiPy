// JavaScript to fetch live data and performance chart (if polling method is used)
function fetchLiveData() {
    fetch('/live-data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('liveScore').innerText = `Score: ${data.score}`;
            const playerStats = document.getElementById('playerStats');
            playerStats.innerHTML = '';
            data.players.forEach(player => {
                playerStats.innerHTML += `<li>${player.name}: ${player.points} points</li>`;
            });
        });
}

// Fetch team performance chart
function fetchTeamPerformanceChart() {
    fetch('/team-performance-chart')
        .then(response => response.json())
        .then(data => {
            document.getElementById('teamPerformanceChart').src = data.chart_path;
        });
}
