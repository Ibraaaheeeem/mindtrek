import okhttp3.*
import java.io.IOException

class RegistrationService {

    private val client = OkHttpClient()

    // Replace with your registration endpoint URL
    private val registrationUrl = "https://your-registration-endpoint.com/register"

    fun registerUser(username: String, password: String, email: String, callback: Callback) {
        val requestBody = FormBody.Builder()
            .add("username", username)
            .add("password", password)
            .add("email", email)
            .build()

        val request = Request.Builder()
            .url(registrationUrl)
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(callback)
    }
}