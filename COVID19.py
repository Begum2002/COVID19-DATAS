import pandas as pd
import plotly.graph_objects as go

# CSV dosyasını yerelden aç
df = pd.read_csv("owid-covid-data.csv")

# Türkiye verilerini filtrele
turkiye = df[df["location"] == "Turkey"].copy()
turkiye['date'] = pd.to_datetime(turkiye['date'])

# 7 günlük hareketli ortalama
turkiye['weekly_cases'] = turkiye['new_cases'].rolling(window=7, min_periods=1).mean()
turkiye['weekly_deaths'] = turkiye['new_deaths'].rolling(window=7, min_periods=1).mean()

# Dalga dönemleri
dalga_donemleri = [
    ('2020-03-11', '2020-06-01'),
    ('2020-09-01', '2021-01-15'),
    ('2021-03-01', '2021-06-15'),
    ('2021-09-01', '2021-12-31')
]

# Kilit tarihler
kilit_tarihler = {
    'İlk Vaka': '2020-03-11',
    'Aşı Başlangıcı': '2021-01-14',
    'Delta Başlangıcı': '2021-07-01'
}

# Grafik oluştur
fig = go.Figure()

# Dalga dönemlerini arka plan gölge olarak ekle
for start, end in dalga_donemleri:
    fig.add_vrect(
        x0=start, x1=end,
        fillcolor="orange", opacity=0.1, line_width=0
    )

# Vaka çizgisi
fig.add_trace(go.Scatter(
    x=turkiye['date'], y=turkiye['weekly_cases'],
    mode='lines+markers',
    name='Haftalık Ortalama Vaka',
    line=dict(color='dodgerblue', width=3),
    marker=dict(size=5),
    hovertemplate='Tarih: %{x|%d %b %Y}<br>Vaka: %{y}<extra></extra>'
))

# Ölüm çizgisi
fig.add_trace(go.Scatter(
    x=turkiye['date'], y=turkiye['weekly_deaths'],
    mode='lines+markers',
    name='Haftalık Ortalama Ölüm',
    line=dict(color='crimson', width=3),
    marker=dict(size=5),
    yaxis='y2',
    hovertemplate='Tarih: %{x|%d %b %Y}<br>Ölüm: %{y}<extra></extra>'
))

# Kilit tarihler için anotasyonlar
for label, date in kilit_tarihler.items():
    y_value = turkiye.loc[turkiye['date']==pd.to_datetime(date), 'weekly_cases'].values[0]
    fig.add_trace(go.Scatter(
        x=[pd.to_datetime(date)],
        y=[y_value],
        mode='markers+text',
        marker=dict(size=12, color='purple', symbol='diamond'),
        text=[label],
        textposition='top center',
        name=label,
        hovertemplate=f'{label}<br>Tarih: {date}<br>Vaka: {y_value}<extra></extra>'
    ))

# Layout ayarları
fig.update_layout(
    title='Türkiye COVID-19 Günlük Vaka ve Ölüm Sayıları (Haftalık Ortalama & Profesyonel)',
    xaxis=dict(title='Tarih', tickformat='%b %Y', tickangle=45),
    yaxis=dict(title='Haftalık Ortalama Vaka', color='dodgerblue'),
    yaxis2=dict(title='Haftalık Ortalama Ölüm', overlaying='y', side='right', color='crimson'),
    template='plotly_white',
    legend=dict(x=0.02, y=0.98, bordercolor='Gray', borderwidth=1),
    hovermode='x unified'
)

# Grafiği interaktif olarak göster
fig.show()

# HTML olarak kaydet (GitHub veya sunum için)
fig.write_html("turkiye_covid19_interactive.html")
