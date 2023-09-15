package com.haneef.medquiz.ui.login

import RegistrationService
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.haneef.medquiz.R
import com.haneef.medquiz.databinding.FragmentHomeBinding
import com.haneef.medquiz.databinding.FragmentLoginBinding
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
            binding.loginLayout.visibility = View.VISIBLE
            // Hide the registration controls
            binding.registerLayout.visibility = View.GONE
        }

        // Handle the click event of the "Register" button
        binding.showRegisterButton.setOnClickListener {
            // Hide the login controls
            binding.loginLayout.visibility = View.GONE
            // Show the registration controls
            binding.registerLayout.visibility = View.VISIBLE
        }

        // You can add code to handle login and registration form submission here
        binding.loginButton.setOnClickListener {
            // Handle login logic
            // Example: Call a login function or validate login credentials
        }

        binding.registerButton.setOnClickListener {
            val username = binding.registerNameEditText.text.toString().trim()
            val email = binding.registerEmailEditText.text.toString().trim()
            val password = binding.registerPasswordEditText.text.toString().trim()
            val password2 = binding.registerPasswordEditText2.text.toString().trim()
            if (
                email != "" &&
                username != "" &&
                password.length >= 4 &&
                password.length < 20 &&
                password == password2
            ) {
                register(email, username, password)
            }
        }

        /*val textView: TextView = binding.textGallery
        galleryViewModel.text.observe(viewLifecycleOwner) {
            textView.text = it
        }*/
        return root
    }

    private fun register(email: String, username: String, password: String) {
        val registrationService = RegistrationService()

        val callback = object : Callback {
            override fun onResponse(call: Call, response: Response) {
                // Handle the response here
                val responseBody = response.body?.string()
                Log.d("USERREG", responseBody.toString())
                // Parse and process the response as needed
            }

            override fun onFailure(call: Call, e: IOException) {
                Log.d("USERREG", e.message.toString())
                // Handle any network or request errors here
            }
        }

        registrationService.registerUser(username, password, email, callback)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}