import com.google.gson.Gson
import com.haneef.medquiz.data.UserData
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import java.io.IOException

class RegistrationService(url: String) {

    private val client = OkHttpClient()

    private val registrationUrl = url

    fun registerUser(userData: UserData, callback: Callback) {
        val gson = Gson()
        val json = gson.toJson(userData)
        val requestBody = RequestBody.create("application/json".toMediaTypeOrNull(), json)
        val request = Request.Builder()
            .url(registrationUrl)
            .post(requestBody)
            .header("Content-Type", "application/x-www-form-urlencoded") // Replace with the appropriate content type if needed
            .build()
        client.newCall(request).enqueue(callback)
    }
}