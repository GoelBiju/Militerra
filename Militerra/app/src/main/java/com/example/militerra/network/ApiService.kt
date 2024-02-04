package com.example.dreamcatch.network

import com.example.militerra.network.ApiResponse
import com.example.militerra.network.analytics
import com.example.militerra.network.command
import com.example.militerra.network.location
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ApiService {

    @POST("location")
    fun location(@Body timeRequest: location): Call<ApiResponse>
    @GET("command")
    fun command(): Call<command>
    @GET("analytics")
    fun analytics(): Call<analytics>

}