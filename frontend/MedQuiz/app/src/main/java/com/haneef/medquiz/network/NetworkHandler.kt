package com.haneef.medquiz.network

import android.content.Context
import android.net.ConnectivityManager
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import com.haneef.medquiz.R
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import java.util.concurrent.TimeUnit

class NetworkHandler(val context: Context, var progressFlag: Boolean) {

    suspend fun fetchWebPageContent(url: String): String {
        var errorMessage = ""
        Log.d("NETWORK", url)

        return withContext(Dispatchers.IO) {
            try {
                    val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
                    val activeNetworkInfo = connectivityManager.activeNetworkInfo

                    if (activeNetworkInfo == null || !activeNetworkInfo.isConnected) {
                        Log.d("NETWORK", "No internet connection")
                        "ERROR"
                    }

                    val client = OkHttpClient.Builder()
                        .callTimeout(30, TimeUnit.SECONDS) // Set the timeout here (e.g., 10 seconds)
                        .build()

                    val request = Request.Builder()
                        .url(url)
                        .build()

                    val response = client.newCall(request).execute()
                // ... IO operations ...
                response.body?.string() ?: "ERROR"
            } catch (e: java.net.SocketTimeoutException) {
                // Handle timeout exception
                errorMessage = "Request time out"
                "ERROR"
            } catch (e: Exception) {
                // Handle other exceptions
                errorMessage = "An error occurred. Please, try again"
                "ERROR"
            }
        }
    }

    fun hasError(responseFromUrl: String): Boolean {
        Log.d("FRONT PAGE", "ERROR")
        return (responseFromUrl == "ERROR")
    }
}