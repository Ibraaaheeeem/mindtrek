import com.google.gson.Gson
import com.haneef.medquiz.data.UserData
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import java.io.IOException

class LoginService(url: String) {

    private val client = OkHttpClient()

    private val loginUrl = url

    fun loginUser(userData: UserData, callback: Callback) {
        val gson = Gson()
        val json = gson.toJson(userData)
        val requestBody = RequestBody.create("application/json".toMediaTypeOrNull(), json)
        val request = Request.Builder()
            .url(loginUrl)
            .post(requestBody)
            .header("Content-Type", "application/x-www-form-urlencoded")
            .build()
        client.newCall(request).enqueue(callback)
    }
}