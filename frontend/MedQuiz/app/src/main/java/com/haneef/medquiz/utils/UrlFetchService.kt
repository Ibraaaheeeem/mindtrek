import com.google.gson.Gson
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull

class UrlFetchService(url: String) {

    private val client = OkHttpClient()

    private val urlToFetch = url

    fun fetchUrl(method: String, userData: Any, callback: Callback) {
        val gson = Gson()
        val json = gson.toJson(userData)
        val requestBody = RequestBody.create("application/json".toMediaTypeOrNull(), json)

        if (method == "POST") {
            val request = Request.Builder()
                .url(urlToFetch)
                .post(requestBody)
                .header("Content-Type", "application/x-www-form-urlencoded")
                .build()
            client.newCall(request).enqueue(callback)
        }
        else if (method == "GET") {
            val request = Request.Builder()
                .url(urlToFetch)
                .get()
                .header("Content-Type", "application/x-www-form-urlencoded")
                .build()
            client.newCall(request).enqueue(callback)
        }

    }
}