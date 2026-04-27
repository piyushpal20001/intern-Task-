import json
import pandas as pd

def generate_dashboard():
    # Load data
    with open('dashboard_data.json', 'r') as f:
        data = json.load(f)
    
    with open('analysis_summary.json', 'r') as f:
        summary = json.load(f)

    # Convert to JS strings
    data_js = json.dumps(data)
    summary_js = json.dumps(summary)

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Influencer Analytics Dashboard - Phase 2</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at top left, #0f172a, #020617);
            color: #f8fafc;
            min-height: 100vh;
        }}
        .glass {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
        }}
        .card-hover:hover {{
            transform: translateY(-5px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.3);
        }}
        .transition-all {{ transition: all 0.3s ease; }}
        .gradient-text {{
            background: linear-gradient(135deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto">
        <!-- Header -->
        <header class="mb-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <h1 class="text-4xl md:text-5xl font-bold mb-2">Influencer <span class="gradient-text">Smart Analytics</span></h1>
                <p class="text-slate-400">Phase 2: AI/ML Prediction & Ranking Dashboard</p>
            </div>
            <div class="flex gap-3">
                <div class="glass px-6 py-3 text-center">
                    <p class="text-xs text-slate-400 uppercase tracking-widest">Total Profiles</p>
                    <p class="text-2xl font-bold text-indigo-400">{summary['total']}</p>
                </div>
                <div class="glass px-6 py-3 text-center">
                    <p class="text-xs text-slate-400 uppercase tracking-widest">Avg Score</p>
                    <p class="text-2xl font-bold text-purple-400">{summary['avg_score']:.1f}</p>
                </div>
            </div>
        </header>

        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="glass p-6 card-hover transition-all">
                <h3 class="text-lg font-semibold mb-4 text-indigo-300">Top Categories</h3>
                <div class="space-y-3" id="category-list">
                    <!-- Categories will be injected here -->
                </div>
            </div>
            <div class="glass p-6 md:col-span-2">
                <h3 class="text-lg font-semibold mb-4 text-purple-300">Performance Distribution</h3>
                <canvas id="scoreChart" height="120"></canvas>
            </div>
        </div>

        <!-- Leaderboard & Scatter -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Leaderboard -->
            <div class="glass p-6 overflow-hidden">
                <h3 class="text-xl font-bold mb-6 flex justify-between items-center">
                    <span>Top 10 Influencers</span>
                    <span class="text-sm font-normal text-slate-400">by Performance Score</span>
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left">
                        <thead>
                            <tr class="text-slate-500 border-b border-white/10">
                                <th class="pb-4 font-medium">Rank</th>
                                <th class="pb-4 font-medium">Influencer</th>
                                <th class="pb-4 font-medium">Category</th>
                                <th class="pb-4 font-medium text-right">Score</th>
                            </tr>
                        </thead>
                        <tbody id="leaderboard-body">
                            <!-- Rows injected here -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Scatter Plot -->
            <div class="glass p-6">
                <h3 class="text-xl font-bold mb-6">Engagement vs. Followers</h3>
                <canvas id="scatterChart"></canvas>
            </div>
        </div>

        <!-- Automation Insight -->
        <div class="mt-8 glass p-8 text-center bg-indigo-500/5 border-indigo-500/20">
             <h3 class="text-2xl font-bold mb-2">Authenticity Analysis</h3>
             <p class="text-slate-400 mb-6">How automation impacts performance scores in our ML model.</p>
             <div class="flex justify-center gap-12">
                <div>
                    <p class="text-sm text-slate-500 uppercase">Manual Avg Score</p>
                    <p class="text-4xl font-bold text-green-400">{summary['automation_impact'].get('No', 0):.1f}</p>
                </div>
                <div class="w-px bg-white/10"></div>
                <div>
                    <p class="text-sm text-slate-500 uppercase">Automated Avg Score</p>
                    <p class="text-4xl font-bold text-red-400">{summary['automation_impact'].get('Yes', 0):.1f}</p>
                </div>
             </div>
        </div>
    </div>

    <script>
        const data = {data_js};
        const summary = {summary_js};

        // Inject Category List
        const catList = document.getElementById('category-list');
        Object.entries(summary.top_categories).slice(0, 5).forEach(([cat, score]) => {{
            const div = document.createElement('div');
            div.className = 'flex justify-between items-center';
            div.innerHTML = `
                <span class="text-slate-300 font-medium">${{cat}}</span>
                <div class="flex items-center gap-2">
                    <div class="w-24 h-2 bg-white/5 rounded-full overflow-hidden">
                        <div class="h-full bg-indigo-500" style="width: ${{score}}%"></div>
                    </div>
                    <span class="text-indigo-400 font-bold">${{score.toFixed(1)}}</span>
                </div>
            `;
            catList.appendChild(div);
        }});

        // Inject Leaderboard
        const lbBody = document.getElementById('leaderboard-body');
        data.slice(0, 10).forEach((item, idx) => {{
            const tr = document.createElement('tr');
            tr.className = 'border-b border-white/5 hover:bg-white/5 transition-all cursor-default';
            tr.innerHTML = `
                <td class="py-4 font-bold text-slate-500">#${{idx + 1}}</td>
                <td class="py-4">
                    <div class="font-bold text-white">${{item.username}}</div>
                    <div class="text-xs text-slate-400">${{item.followers.toLocaleString()}} followers</div>
                </td>
                <td class="py-4 text-slate-300 text-sm">${{item.category}}</td>
                <td class="py-4 text-right">
                    <span class="px-3 py-1 glass bg-indigo-500/10 text-indigo-300 rounded-lg font-bold">${{item.performance_score}}</span>
                </td>
            `;
            lbBody.appendChild(tr);
        }});

        // Score Bar Chart
        new Chart(document.getElementById('scoreChart'), {{
            type: 'bar',
            data: {{
                labels: data.slice(0, 15).map(i => i.username),
                datasets: [{{
                    label: 'Performance Score',
                    data: data.slice(0, 15).map(i => i.performance_score),
                    backgroundColor: 'rgba(129, 140, 248, 0.6)',
                    borderColor: '#818cf8',
                    borderWidth: 1,
                    borderRadius: 8
                }}]
            }},
            options: {{
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ beginAtZero: true, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        // Scatter Chart
        new Chart(document.getElementById('scatterChart'), {{
            type: 'scatter',
            data: {{
                datasets: [{{
                    label: 'Influencers',
                    data: data.map(i => ({{ x: i.followers, y: i['engagement_rate (%)'] }})),
                    backgroundColor: 'rgba(192, 132, 252, 0.6)'
                }}]
            }},
            options: {{
                scales: {{
                    x: {{ 
                        type: 'logarithmic',
                        title: {{ display: true, text: 'Followers (Log Scale)', color: '#94a3b8' }},
                        grid: {{ color: 'rgba(255,255,255,0.05)' }}
                    }},
                    y: {{ 
                        title: {{ display: true, text: 'Engagement %', color: '#94a3b8' }},
                        grid: {{ color: 'rgba(255,255,255,0.05)' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
    """
    
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Dashboard generated successfully: dashboard.html")

if __name__ == "__main__":
    generate_dashboard()
