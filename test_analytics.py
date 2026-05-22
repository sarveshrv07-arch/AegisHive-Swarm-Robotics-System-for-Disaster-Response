from analytics import Analytics

analytics = Analytics()

battery_values = [
    100,
    95,
    90,
    85,
    80,
    75,
    70
]

analytics.battery_chart(
    battery_values
)
