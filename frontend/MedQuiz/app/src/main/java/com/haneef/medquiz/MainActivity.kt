package com.haneef.medquiz

import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.View
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.ActionBarDrawerToggle
import androidx.appcompat.app.AppCompatActivity
import androidx.drawerlayout.widget.DrawerLayout
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.google.android.material.navigation.NavigationView
import com.haneef.medquiz.databinding.ActivityMainBinding
import com.haneef.medquiz.utils.PrefsManager

class MainActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityMainBinding

    fun getBinding(): ActivityMainBinding? {
        return binding
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        PrefsManager.getInstance(this).saveQuizMode("FREE_MODE")
        val signButton = binding.navView.getHeaderView(0).findViewById<Button>(R.id.signButton)
        signButton.setOnClickListener{
            when((it as Button).text){
                "SIGN OUT" -> {
                    PrefsManager.getInstance(this).clearJwt()
                    refreshProfileOnDrawer()
                }
                "SIGN IN" -> {
                    findNavController(R.id.nav_host_fragment_content_main).navigate(R.id.nav_login)

                }
            }
        }
        setContentView(binding.root)

        setSupportActionBar(binding.appBarMain.toolbar)

        /*binding.appBarMain.fab.setOnClickListener { view ->
            Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                .setAction("Action", null).show()
        }*/
        val drawerLayout: DrawerLayout = binding.drawerLayout
        val navView: NavigationView = binding.navView
        val navController = findNavController(R.id.nav_host_fragment_content_main)
        val toggle = ActionBarDrawerToggle(
            this,
            drawerLayout,
            R.string.navigation_drawer_open,
            R.string.navigation_drawer_close
        )
        drawerLayout.addDrawerListener(toggle);
        toggle.syncState();
        drawerLayout.addDrawerListener(object: DrawerLayout.DrawerListener{
            override fun onDrawerSlide(drawerView: View, slideOffset: Float) {
            }

            override fun onDrawerOpened(drawerView: View) {
                refreshProfileOnDrawer()
            }

            override fun onDrawerClosed(drawerView: View) {

            }

            override fun onDrawerStateChanged(newState: Int) {

            }

        })
        binding.navView.getHeaderView(0).findViewById<Button>(R.id.viewProfile).setOnClickListener{
            findNavController(R.id.nav_host_fragment_content_main).navigate(R.id.nav_profile)
        }
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        appBarConfiguration = AppBarConfiguration(
            setOf(
                R.id.nav_home, R.id.nav_login, R.id.nav_slideshow
            ), drawerLayout
        )
        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)

        refreshProfileOnDrawer()
    }

    private fun refreshProfileOnDrawer() {
        val username = PrefsManager.getInstance(this).getUsername()
        val useremail = PrefsManager.getInstance(this).getUserEmail()

        if ((username == "GUEST" && useremail == "no email")){
            binding.navView.getHeaderView(0).findViewById<Button>(R.id.viewProfile).visibility = View.GONE
            binding.navView.getHeaderView(0).findViewById<Button>(R.id.signButton).text = "SIGN IN"
        }
        else {
            binding.navView.getHeaderView(0).findViewById<Button>(R.id.viewProfile).visibility = View.VISIBLE
            binding.navView.getHeaderView(0).findViewById<Button>(R.id.signButton).text = "SIGN OUT"
        }
        binding.navView.getHeaderView(0).findViewById<TextView>(R.id.useremail).text = useremail
        binding.navView.getHeaderView(0).findViewById<TextView>(R.id.username).text = username
        Log.d("PROFILE", "REFRESH")

    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.main, menu)
        return true
    }

    override fun onSupportNavigateUp(): Boolean {
        refreshProfileOnDrawer()
        val navController = findNavController(R.id.nav_host_fragment_content_main)
        return navController.navigateUp(appBarConfiguration) || super.onSupportNavigateUp()
    }
}