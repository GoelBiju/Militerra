package com.example.dreamcatch.network

import android.content.Context
import com.example.militerra.R
import okhttp3.CertificatePinner
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.InputStream
import java.security.KeyStore
import java.security.cert.CertificateFactory
import java.security.cert.X509Certificate
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManagerFactory
import javax.net.ssl.X509TrustManager
import okhttp3.logging.HttpLoggingInterceptor

object Client {
    private val URL = "https://fd82-2a0c-5bc0-40-3e3a-f866-b6b3-8188-5317.ngrok-free.app/"
    private lateinit var retrofit: Retrofit

    fun init(context: Context) {
        val loggingInterceptor = HttpLoggingInterceptor()
        loggingInterceptor.level = HttpLoggingInterceptor.Level.BODY

        val trustAllCertificatesManager = object : X509TrustManager {
            override fun checkClientTrusted(chain: Array<out X509Certificate>?, authType: String?) {
                // No implementation needed for client verification
            }

            override fun checkServerTrusted(chain: Array<out X509Certificate>?, authType: String?) {
                // Accept all certificates
            }

            override fun getAcceptedIssuers(): Array<X509Certificate> {
                return arrayOf()  // Return an empty array to trust all issuers
            }
        }

        val sslContext = SSLContext.getInstance("TLS")
        sslContext.init(null, arrayOf(trustAllCertificatesManager), null)

        val client = OkHttpClient.Builder()
            .sslSocketFactory(sslContext.socketFactory, trustAllCertificatesManager)
            .hostnameVerifier { _, _ -> true }  // Bypass hostname verification
            .addInterceptor(loggingInterceptor)
            .build()

        retrofit = Retrofit.Builder()
            .baseUrl(URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    fun getApiService(): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}
