package com.example.militerra.network


data class location(val latitude: Double, val longitude: Double)

data class command(val command: String)

data class analytics(
    val overall_score: String,
    val hydration: String,
    val muscle_mass: String,
    val body_fat: String,
    val max_speed: String,
    val sleep: String,
    val stress: String
)


