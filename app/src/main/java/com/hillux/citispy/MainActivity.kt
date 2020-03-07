package com.hillux.citispy

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

import android.widget.Toast
import android.content.Intent
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.EditText
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.AdditionalUserInfo

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

