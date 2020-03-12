package com.hillux.citispy

import android.R
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupWithNavController
import com.google.android.material.navigation.NavigationView
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser


class MainActivity : AppCompatActivity() {
    private var btnTagUser: Button? = null
    private var btnRaiseAlarm: Button? = null
    private var editProfile: Button? = null

    private var progressBar: ProgressBar? = null

    private var authListener: FirebaseAuth.AuthStateListener? = null
    private var auth: FirebaseAuth? = null
    private var user: FirebaseUser? = null


    val firebaseAuth = FirebaseAuth.getInstance()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        auth = FirebaseAuth.getInstance()
        user = FirebaseAuth.getInstance().currentUser

        setSupportActionBar(findViewById(R.id.app_bar))
        val navController = findNavController(R.id.nav_host_fragment)
        val appBarConfiguration = AppBarConfiguration(navController.graph)
        findViewById<Toolbar>(R.id.toolbar)
            .setupWithNavController(navController, appBarConfiguration)

// There is usually only 1 header view.
// Multiple header views can technically be added at runtime.
// We can use navigationView.getHeaderCount() to determine the total number.
        // There is usually only 1 header view.
// Multiple header views can technically be added at runtime.
// We can use navigationView.getHeaderCount() to determine the total number.

        // Lookup navigation view
        // Lookup navigation view
        val navigationView =
            findViewById<View>(R.id.navView) as NavigationView
// Inflate the header view at runtime
// Inflate the header view at runtime
        val headerLayout = navigationView.inflateHeaderView(R.layout.nav_header)
        if (navigtationView.getHeaderCount() > 0) {
            // avoid NPE by first checking if there is at least one Header View available
            val headerLayout: View = navigationView.getHeaderView(0)
        }
    }

    override fun onStart() {
        super.onStart()
        firebaseAuth!!.addAuthStateListener (this.authStateListener);
    }
    val authStateListener = FirebaseAuth.AuthStateListener { firebaseAuth ->
        val currentUser = firebaseAuth.currentUser

        if (currentUser == null) {
            startActivity(Intent(this, LoginRegisterActivity::class.java))
            finish()
        }
    }

    private fun raiseAlarm(user: FirebaseUser){

    }
    private fun tagUser(user: FirebaseUser){

    }
}

