import com.google.gson.Gson
import com.haneef.medquiz.data.MockData
import com.haneef.medquiz.data.UserData
import okhttp3.Callback
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import java.io.IOException

class MockSetup(url: String, token: String) {

    private val client = OkHttpClient()

    private val createMockUrl = url
    private val token = token

    fun createMock(mockData: MockData, callback: Callback) {
        val gson = Gson()
        val json = gson.toJson(mockData)
        val requestBody = RequestBody.create("application/json".toMediaTypeOrNull(), json)
        val request = Request.Builder()
            .url(createMockUrl)
            .post(requestBody)
            .header("Content-Type", "application/x-www-form-urlencoded")
            .header("Authorization", "Bearer $token")
            .build()
        client.newCall(request).enqueue(callback)
    }
}