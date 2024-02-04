package com.example.militerra

import android.app.Application
import com.example.dreamcatch.network.Client

class App : Application() {

    override fun onCreate() {
        super.onCreate()
        Client.init(this)
    }
}
