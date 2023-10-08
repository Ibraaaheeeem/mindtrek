package com.haneef.medquiz.ui.login

import UrlFetchService
import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.google.gson.Gson
import com.haneef.medquiz.MainActivity
import com.haneef.medquiz.R
import com.haneef.medquiz.data.BackendResponse
import com.haneef.medquiz.data.UserData
import com.haneef.medquiz.databinding.FragmentHomeBinding
import com.haneef.medquiz.databinding.FragmentLoginBinding
import com.haneef.medquiz.utils.AlertUtils
import com.haneef.medquiz.utils.PrefsManager
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.Call
import okhttp3.Callback
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import java.io.IOException

class LoginFragment : Fragment() {

    private var _binding: FragmentLoginBinding? = null
    private val REGISTRATION_ENDPOINT = "/auth/register"
    private val LOGIN_ENDPOINT = "/auth/login"
    private val client = OkHttpClient()

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        _binding = FragmentLoginBinding.inflate(inflater, container, false)
        val root: View = binding.root

        binding.loginLayout.visibility = View.VISIBLE
        binding.registerLayout.visibility = View.GONE

        // Handle the click event of the "Login" button
        binding.showLoginButton.setOnClickListener {
            // Show the login controls
            binding.showRegisterButton.setBackgroundColor(Color.argb(127, 0,0,0))
            binding.showLoginButton.setBackgroundColor(Color.argb(127, 0,0,255))
            binding.loginLayout.visibility = View.VISIBLE
            // Hide the registration controls
            binding.registerLayout.visibility = View.GONE
        }

        // Handle the click event of the "Register" button
        binding.showRegisterButton.setOnClickListener {
            // Hide the login controls
            binding.loginLayout.visibility = View.GONE
            binding.showLoginButton.setBackgroundColor(Color.argb(127, 0,0,0))
            binding.showRegisterButton.setBackgroundColor(Color.argb(127, 0,0,255))
            // Show the registration controls
            binding.registerLayout.visibility = View.VISIBLE
        }

        // You can add code to handle login and registration form submission here
        binding.loginButton.setOnClickListener {
            // Handle login logic
            // Example: Call a login function or validate login credentials
            val email = binding.loginEmailEditText.text.toString().trim()
            val password = binding.loginPasswordEditText.text.toString().trim()
            if (
                isValidEmail(email)&&
                password.length >= 4 &&
                password.length < 20
            ) {
                val userData = UserData("", password, email)
                login(userData)
            }
        }

        binding.registerButton.setOnClickListener {
            val username = binding.registerNameEditText.text.toString().trim()
            val email = binding.registerEmailEditText.text.toString().trim()
            val password = binding.registerPasswordEditText.text.toString().trim()
            val password2 = binding.registerPasswordEditText2.text.toString().trim()
            Log.d("USERREG", "B4B4")
            if (
                isValidEmail(email) &&
                username != "" &&
                password.length >= 4 &&
                password.length < 20 &&
                password == password2
            ) {
                val userData = UserData(username, password, email)
                register(userData)
            }
        }

        /*val textView: TextView = binding.textGallery
        galleryViewModel.text.observe(viewLifecycleOwner) {
            textView.text = it
        }*/
        binding.showRegisterButton.setBackgroundColor(Color.argb(127, 0,0,0))
        return root
    }

    private fun isValidEmail(email: String): Boolean {
        if (email == ""){
            alert("Invalid Email")
            return false
        }
        else if (!email.contains("@") || !email.contains(".")){
            alert("Invalid Email")
            return false
        }
        return true
    }

    private fun alert(message: String) {
        val myAlert = AlertUtils(requireContext())
        myAlert.showAlert(message, message,"OK")
    }

    private fun login(userData: UserData) {
        val url = "${resources.getString(R.string.root_url)}${LOGIN_ENDPOINT}"
        val loginService = UrlFetchService(url)
        val callback = object : Callback {
            override fun onResponse(call: Call, response: Response) {
                // Handle the response here
                val responseBody = response.body?.string()
                Log.d("USERREG", responseBody.toString())
                val gson = Gson()

                val response = gson.fromJson(responseBody.toString(), BackendResponse::class.java)

                val token = response.access_token
                if (token != ""){
                    val alertUtils = AlertUtils(requireContext()) // 'this' is the context of your activity or fragment
                    // Display an alert
                    val myScope = CoroutineScope(Dispatchers.Main)
                    myScope.launch {
                        PrefsManager.getInstance(requireContext()).saveJwt(token)
                        PrefsManager.getInstance(requireContext()).saveUserEmail(response.useremail)
                        PrefsManager.getInstance(requireContext()).saveUsername(response.username)

                        alertUtils.showAlert("Log in Successfful", "You have successfully logged in", "OK"){
                            findNavController().navigate(R.id.login_to_home)
                        }
                    }
                    Log.d("USERREG", token)
                }
                else{
                    val alertUtils = AlertUtils(requireContext())
                    val myScope = CoroutineScope(Dispatchers.Main)
                    myScope.launch {
                        PrefsManager.getInstance(requireContext()).saveJwt(token)
                        alertUtils.showAlert("Incorrect Login details", "Username or password incorrect", "OK"){
                            findNavController().navigate(R.id.login_to_home)
                        }
                    }
                }

            }

            override fun onFailure(call: Call, e: IOException) {
                Log.d("USERREG", e.message.toString())
                // Handle any network or request errors here
            }
        }

        loginService.fetchUrl("POST", userData, callback)
    }

    private fun register(userData: UserData) {
        val url = "${resources.getString(R.string.root_url)}${REGISTRATION_ENDPOINT}"
        val registrationService = UrlFetchService(url)
        Log.d("USERREG", "BEFORE: "+ url)
        val callback = object : Callback {
            override fun onResponse(call: Call, response: Response) {
                // Handle the response here
                val responseBody = response.body?.string()
                val gson = Gson()
                val response = gson.fromJson(responseBody, BackendResponse::class.java)

                val message = response.message
                if (message.equals("Registration successful")){
                    val alertUtils = AlertUtils(requireContext()) // 'this' is the context of your activity or fragment
                    // Display an alert
                    val myScope = CoroutineScope(Dispatchers.Main)
                    myScope.launch {
                        alertUtils.showAlert(
                            "Registration Successfful",
                            "We have received your registration. Now, you can log in.",
                            "OK"
                        ){
                            binding.loginButton.performClick()
                        }
                    }
                }
                println("Message: $message")
            }

            override fun onFailure(call: Call, e: IOException) {
                Log.d("USERREG", e.message.toString())
                // Handle any network or request errors here
            }
        }

        registrationService.fetchUrl("POST",userData, callback)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}