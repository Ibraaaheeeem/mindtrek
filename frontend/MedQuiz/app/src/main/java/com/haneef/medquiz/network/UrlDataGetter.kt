package com.haneef.medquiz.network

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.coroutineScope
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.IOException

class UrlDataGetter {
    private val client = OkHttpClient()
    suspend fun fetchDataFromUrl(url: String): String? {
        return try {

            val response = withContext(Dispatchers.IO) {
                // Make the HTTP request here
                try {
                    val request = Request.Builder()
                        .url(url)
                        .build()

                    val response = client.newCall(request).execute()
                    val json = response.body?.string()
                    json

//                    // Use Gson to parse the JSON into your data class
//                    return gson.fromJson(json, Array<Book>::class.java).toList()
                } catch (e: IOException) {
                    null
                }
            }
            response
        } catch (e: Exception) {
            null
        }
    }
}
