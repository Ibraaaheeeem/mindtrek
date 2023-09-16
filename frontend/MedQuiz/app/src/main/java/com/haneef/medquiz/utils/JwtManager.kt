package com.haneef.medquiz.utils

import android.content.Context
import android.content.SharedPreferences

class JwtManager private constructor(context: Context) {

    private val sharedPreferences: SharedPreferences

    init {
        sharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }

    companion object {
        private const val PREFS_NAME = "MyPrefs"
        private const val KEY_JWT = "jwt_token"

        @Volatile
        private var instance: JwtManager? = null

        fun getInstance(context: Context): JwtManager {
            return instance ?: synchronized(this) {
                instance ?: JwtManager(context).also { instance = it }
            }
        }
    }

    fun saveJwt(jwt: String) {
        sharedPreferences.edit().putString(KEY_JWT, jwt).apply()
    }

    fun getJwt(): String? {
        return sharedPreferences.getString(KEY_JWT, null)
    }

    fun clearJwt() {
        sharedPreferences.edit().remove(KEY_JWT).apply()
    }
}
