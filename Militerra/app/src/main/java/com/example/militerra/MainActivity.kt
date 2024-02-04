package com.example.militerra

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.dreamcatch.network.Client
import com.example.militerra.network.ApiResponse
import com.example.militerra.network.analytics
import com.example.militerra.network.location
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

@SuppressLint("UseSwitchCompatOrMaterialCode")
class MainActivity : AppCompatActivity() {
    private lateinit var overall: TextView
    private lateinit var hydration: TextView
    private lateinit var musclemass: TextView
    private lateinit var bodyfat: TextView
    private lateinit var maxspeed: TextView
    private lateinit var sleep: TextView
    private lateinit var stress: TextView


    private val handler = Handler(Looper.getMainLooper())
    private val locationUpdateInterval = 5000L // Update location every 5 seconds
    private var lastKnownLocation: Location? = null

    @RequiresApi(Build.VERSION_CODES.O)
    @SuppressLint("SetTextI18n")
    public override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        overall = findViewById(R.id.textView25)
        hydration = findViewById(R.id.textView12)
        musclemass = findViewById(R.id.textView13)
        bodyfat = findViewById(R.id.textView14)
        maxspeed = findViewById(R.id.textView20)
        sleep = findViewById(R.id.textView21)
        stress = findViewById(R.id.textView22)

        val apiService = Client.getApiService()
        val call = apiService.analytics()
        call.enqueue(object : Callback<analytics> {
            override fun onResponse(call: Call<analytics>, response: Response<analytics>) {
                val analytics = response.body()

                if (response.isSuccessful) {
                    overall.text = analytics?.overall_score
                    hydration.text = analytics?.hydration
                    musclemass.text = analytics?.muscle_mass
                    bodyfat.text = analytics?.body_fat
                    maxspeed.text = analytics?.max_speed
                    sleep.text = analytics?.sleep
                    stress.text = analytics?.stress
                    Log.d("RetrofitDebug", "API call successful. Analytics data: $analytics")
                } else {
                    Log.d("RetrofitDebug", "API call successful. Analytics data: $analytics")

                    Log.e("RetrofitDebug", "API call failed: ${response.code()}")
                }
            }

            override fun onFailure(call: Call<analytics>, t: Throwable) {
                Log.e("RetrofitDebug", "API call failed: ${t.message}")
            }
        })

        startLocationUpdates()

        // Schedule periodic location updates
        handler.postDelayed(locationUpdateRunnable, locationUpdateInterval)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun getLocation()                                                                                      {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            val locationManager = getSystemService(LOCATION_SERVICE) as android.location.LocationManager?
            lastKnownLocation = locationManager?.getLastKnownLocation(LocationManager.GPS_PROVIDER)
            lastKnownLocation?.let {
                val latitude = it.latitude
                val longitude = it.longitude
                Log.d(TAG, "Location: Latitude: $latitude, Longitude: $longitude")
                val locationText = "Location: Latitude: $latitude, Longitude: $longitude"

                val locationRequest = location(latitude, longitude)
                val apiService = Client.getApiService()
                val call = apiService.location(locationRequest)
                call.enqueue(object : Callback<ApiResponse> {
                    override fun onResponse(call: Call<ApiResponse>, response: Response<ApiResponse>) {
                        if (response.isSuccessful) {
                            Log.d("RetrofitDebug", "API call successful")
                        } else {
                            Log.e("RetrofitDebug", "API call failed: ${response.code()}")
                        }
                    }

                    override fun onFailure(call: Call<ApiResponse>, t: Throwable) {
                        Log.e("RetrofitDebug", "API call failed: ${t.message}")
                    }
                })
            }
        } else {
            Log.d(TAG, "Location permission not granted.")
        }
    }

    public override fun onDestroy() {
        stopLocationUpdates()
        super.onDestroy()
    }

    public override fun onResume() {
        super.onResume()
    }

    private val locationUpdateRunnable = object : Runnable {
        @RequiresApi(Build.VERSION_CODES.O)
        override fun run() {
            // Check location permission and get location
            checkLocationPermission()

            // Schedule the next location update
            handler.postDelayed(this, locationUpdateInterval)
        }
    }

    private fun startLocationUpdates() {
        handler.post(locationUpdateRunnable)
    }

    private fun stopLocationUpdates() {
        handler.removeCallbacks(locationUpdateRunnable)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun checkLocationPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            getLocation()
        } else {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), LOCATION_PERMISSION_REQUEST_CODE)
        }
    }

    companion object {
        const val TAG = "Terra"
        private const val LOCATION_PERMISSION_REQUEST_CODE = 1001
    }
}
