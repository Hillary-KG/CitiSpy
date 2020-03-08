package com.hillux.citispy

import android.content.Intent
import android.os.Bundle
import android.text.TextUtils
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.isVisible
import com.google.android.material.snackbar.Snackbar
import com.google.firebase.FirebaseException
import com.google.firebase.FirebaseTooManyRequestsException
import com.google.firebase.auth.*
import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.firestore.FirebaseFirestore
import java.util.concurrent.TimeUnit
import kotlinx.android.synthetic.main.activity_login_register.buttonResend
import kotlinx.android.synthetic.main.activity_login_register.buttonStartVerification
import kotlinx.android.synthetic.main.activity_login_register.buttonVerifyPhone
import kotlinx.android.synthetic.main.activity_login_register.progressBar
//import kotlinx.android.synthetic.main.activity_login_register.inputEmail
import kotlinx.android.synthetic.main.activity_login_register.inputFirstName
import kotlinx.android.synthetic.main.activity_login_register.inputLastName
import kotlinx.android.synthetic.main.activity_login_register.inputPhoneNumber
import kotlinx.android.synthetic.main.activity_login_register.fieldVerificationCode
import kotlinx.android.synthetic.main.activity_login_register.authButtons
import kotlinx.android.synthetic.main.activity_login_register.phoneAuthFields


class LoginRegisterActivity: AppCompatActivity(), View.OnClickListener {
    // [START declare_auth]
    private lateinit var auth: FirebaseAuth
    private lateinit var database: DatabaseReference
    // [END declare_auth]

//    private var inputFirstName: EditText? = null
//    private var inputLastName: EditText? = null
//    private var inputPhoneNumber: EditText? = null
//
//    private var inputEmail: EditText? = null
//    private var inputPassword: EditText? = null
//    private var progressBar: ProgressBar? = null
//    private var buttonStartVerification: Button? = null
//    private var buttonVerifyPhone: Button? = null
//    private var buttonResend: Button? = null

    private var storedVerificationId: String? = null
    private lateinit var resendToken: PhoneAuthProvider.ForceResendingToken
    private lateinit var callbacks: PhoneAuthProvider.OnVerificationStateChangedCallbacks
    private var verificationInProgress = false




    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login_register)

        // Restore instance state
        if (savedInstanceState != null) {
            onRestoreInstanceState(savedInstanceState)
        }

        // Assign click listeners
        buttonStartVerification!!.setOnClickListener(this)
        buttonVerifyPhone!!.setOnClickListener(this)
        buttonResend!!.setOnClickListener(this)
//        progressBar = findViewById(R.id.progressBar)
        // signOutButton.setOnClickListener(this)

        // [START initialize_auth]
        // Initialize Firebase Auth
        auth = FirebaseAuth.getInstance()
        // [END initialize_auth]

        // [START initialize_database]
        // Initialize Firebase DB
        database = FirebaseDatabase.getInstance().reference
        // [END initialize_auth]


        // Initialize phone auth callbacks
        // [START phone_auth_callbacks]
        callbacks = object : PhoneAuthProvider.OnVerificationStateChangedCallbacks() {

            override fun onVerificationCompleted(credential: PhoneAuthCredential) {
                // This callback will be invoked in two situations:
                // 1 - Instant verification. In some cases the phone number can be instantly
                //     verified without needing to send or enter a verification code.
                // 2 - Auto-retrieval. On some devices Google Play services can automatically
                //     detect the incoming verification SMS and perform verification without
                //     user action.
                Log.d(TAG, "onVerificationCompleted:$credential")
                // [START_EXCLUDE silent]
                verificationInProgress = false
                // [END_EXCLUDE]

                // [START_EXCLUDE silent]
                // Update the UI and attempt sign in with the phone credential
                updateUI(STATE_VERIFY_SUCCESS, credential)
                // [END_EXCLUDE]
                signInWithPhoneAuthCredential(credential)
            }

            override fun onVerificationFailed(e: FirebaseException) {
                // This callback is invoked in an invalid request for verification is made,
                // for instance if the the phone number format is not valid.
                Log.w(TAG, "onVerificationFailed", e)
                // [START_EXCLUDE silent]
                verificationInProgress = false
                // [END_EXCLUDE]

                if (e is FirebaseAuthInvalidCredentialsException) {
                    // Invalid request
                    // [START_EXCLUDE]
                    inputPhoneNumber!!.error = "Invalid phone number."
                    // [END_EXCLUDE]
                } else if (e is FirebaseTooManyRequestsException) {
                    // The SMS quota for the project has been exceeded
                    // [START_EXCLUDE]
                    Snackbar.make(findViewById(android.R.id.content), "Quota exceeded.",
                        Snackbar.LENGTH_SHORT).show()
                    // [END_EXCLUDE]
                }

                // Show a message and update the UI
                // [START_EXCLUDE]
                updateUI(STATE_VERIFY_FAILED)
                // [END_EXCLUDE]
            }

            override fun onCodeSent(
                verificationId: String,
                token: PhoneAuthProvider.ForceResendingToken
            ) {
                // The SMS verification code has been sent to the provided phone number, we
                // now need to ask the user to enter the code and then construct a credential
                // by combining the code with a verification ID.
                Log.d(TAG, "onCodeSent:$verificationId")

                // Save verification ID and resending token so we can use them later
                storedVerificationId = verificationId
                resendToken = token

                // [START_EXCLUDE]
                // Update UI
                updateUI(STATE_CODE_SENT)
                // [END_EXCLUDE]
            }
        }
        // [END phone_auth_callbacks]
    }

    // [START on_start_check_user]
    override fun onStart() {
        super.onStart()
        // Check if user is signed in (non-null) and update UI accordingly.
        val currentUser = auth.currentUser
        updateUI(currentUser)

        // [START_EXCLUDE]
        if (verificationInProgress && validatePhoneNumber()) {
            startPhoneNumberVerification(inputPhoneNumber!!.text.toString())
        }
        // [END_EXCLUDE]
    }
    // [END on_start_check_user]

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putBoolean(KEY_VERIFY_IN_PROGRESS, verificationInProgress)
    }

    override fun onRestoreInstanceState(savedInstanceState: Bundle) {
        super.onRestoreInstanceState(savedInstanceState)
        verificationInProgress = savedInstanceState.getBoolean(KEY_VERIFY_IN_PROGRESS)
    }

    private fun saveUser(user: FirebaseUser?){
        if (user != null){
            var userDetails: Map<String, String> = mapOf(
                "first_name" to inputFirstName!!.toString(),
                "last_name" to inputLastName!!.toString(),
//                "email_address" to inputEmail!!.toString(),
                "phone_number" to inputPhoneNumber!!.toString()
                )
            database.child("users").child(user.uid).setValue(userDetails)
        }
    }
    private fun startPhoneNumberVerification(phoneNumber: String) {
        // [START start_phone_auth]
        buttonVerifyPhone.visibility = View.GONE
        PhoneAuthProvider.getInstance().verifyPhoneNumber(
            phoneNumber, // Phone number to verify
            60, // Timeout duration
            TimeUnit.SECONDS, // Unit of timeout
            this, // Activity (for callback binding)
            callbacks) // OnVerificationStateChangedCallbacks
        // [END start_phone_auth]


        verificationInProgress = true
    }

    private fun verifyPhoneNumberWithCode(verificationId: String?, code: String) {
        // [START verify_with_code]
        val credential = PhoneAuthProvider.getCredential(verificationId!!, code)
        // [END verify_with_code]
        signInWithPhoneAuthCredential(credential)
    }

    // [START resend_verification]
    private fun resendVerificationCode(
        phoneNumber: String,
        token: PhoneAuthProvider.ForceResendingToken?
    ) {
        PhoneAuthProvider.getInstance().verifyPhoneNumber(
            phoneNumber, // Phone number to verify
            60, // Timeout duration
            TimeUnit.SECONDS, // Unit of timeout
            this, // Activity (for callback binding)
            callbacks, // OnVerificationStateChangedCallbacks
            token) // ForceResendingToken from callbacks
    }
    // [END resend_verification]

    // [START sign_in_with_phone]
    private fun signInWithPhoneAuthCredential(credential: PhoneAuthCredential) {
        auth.signInWithCredential(credential)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    var message:String = "Registration successful!"
                    // Sign in success, update UI with the signed-in user's information
                    Log.d(TAG, "signInWithCredential:success")

                    val user = task.result?.user
                    val myToast: Toast = Toast.makeText(applicationContext, message, Toast.LENGTH_SHORT)
                    myToast.show()
//                    val snackBar: Snackbar = Snackbar.make(findViewById(R.id.parent), message, Snackbar.LENGTH_LONG)
//                    snackBar.setAction("Dismiss", View.OnClickListener {
//
//                    })
//                    snackBar.show()
                    // [START_EXCLUDE]
//                    val intent = Intent(this@LoginRegisterActivity, MainActivity::class.java)
//                    startActivity(intent)
//                    finish()
                    saveUser(user)
                    updateUI(STATE_SIGNIN_SUCCESS, user)
                    // [END_EXCLUDE]
                } else {
                    var message: String = "Something went wrong,please try again"
                    // Sign in failed, display a message and update the UI
                    Log.w(TAG, "signInWithCredential:failure", task.exception)
                    if (task.exception is FirebaseAuthInvalidCredentialsException) {
                        // The verification code entered was invalid
                        // [START_EXCLUDE silent]
                        fieldVerificationCode!!.error = "Invalid code."
                        // [END_EXCLUDE]
                        message = "Invalid code."
                    }
                    val myToast: Toast = Toast.makeText(applicationContext, message, Toast.LENGTH_SHORT)
                    myToast.show()

//                    val snackBar: Snackbar = Snackbar.make(findViewById(R.id.parent), message, Snackbar.LENGTH_LONG)
//                    snackBar.setAction("Dismiss", View.OnClickListener {
//
//                    })
//                    snackBar.show()
                    // [START_EXCLUDE silent]
                    // Update UI
                    updateUI(STATE_SIGNIN_FAILED)
                    // [END_EXCLUDE]
                }
            }
    }
    // [END sign_in_with_phone]

    private fun signOut() {
        auth.signOut()
        updateUI(STATE_INITIALIZED)
    }

    private fun updateUI(user: FirebaseUser?) {
        if (user != null) {
            updateUI(STATE_SIGNIN_SUCCESS, user)
        } else {
            updateUI(STATE_INITIALIZED)
        }
    }

    private fun updateUI(uiState: Int, cred: PhoneAuthCredential) {
        updateUI(uiState, null, cred)
    }

    private fun updateUI(
        uiState: Int,
        user: FirebaseUser? = auth.currentUser,
        cred: PhoneAuthCredential? = null
    ) {
        when (uiState) {
            STATE_INITIALIZED -> {
                // Initialized state, show only the phone number field and start button
                enableViews(buttonStartVerification, inputPhoneNumber)
                disableViews(buttonVerifyPhone, buttonResend, fieldVerificationCode)
//                detail.setText(null)
            }
            STATE_CODE_SENT -> {
                // Code sent state, show the verification field, the
                enableViews(buttonVerifyPhone, buttonResend, inputPhoneNumber, fieldVerificationCode)
                disableViews(buttonStartVerification)
//                detail.setText(R.string.status_code_sent)
            }
            STATE_VERIFY_FAILED -> {
                // Verification has failed, show all options
                enableViews(buttonStartVerification, buttonVerifyPhone, buttonResend, inputPhoneNumber,
                    fieldVerificationCode)
//                detail.setText(R.string.status_verification_failed)
            }
            STATE_VERIFY_SUCCESS -> {
                // Verification has succeeded, proceed to firebase sign in
                disableViews(buttonStartVerification, buttonVerifyPhone, buttonResend, inputPhoneNumber,
                    fieldVerificationCode)
//                detail.setText(R.string.status_verification_succeeded)

                // Set the verification text based on the credential
                if (cred != null) {
                    if (cred.smsCode != null) {
                        fieldVerificationCode!!.setText(cred.smsCode)
                    } else {
                        fieldVerificationCode!!.setText(R.string.instant_validation)
                    }
                }
            }
            STATE_SIGNIN_FAILED ->{
                val message: String = "Oops! registration failed. Please try again"
                val myToast: Toast = Toast.makeText(applicationContext, message, Toast.LENGTH_SHORT)
                myToast.show()

                enableViews(buttonStartVerification, inputPhoneNumber)
                disableViews(buttonVerifyPhone, buttonResend, fieldVerificationCode)
//                detail.setText(R.string.status_sign_in_failed)
            }

            STATE_SIGNIN_SUCCESS -> {
                val intent = Intent(this@LoginRegisterActivity, MainActivity::class.java)
                    startActivity(intent)
                    finish()
            }
        } // Np-op, handled by sign-in check

        if (user == null) {
            // Signed out
            phoneAuthFields.visibility = View.VISIBLE
//            authButtons.visibility = View.VISIBLE
            buttonVerifyPhone.visibility = View.GONE
            buttonResend.visibility = View.GONE
            buttonResend.isEnabled = false
            buttonResend.isClickable = false


//            status.setText(R.string.signed_out)
        } else {
            // Signed in
            phoneAuthFields.visibility = View.GONE
            authButtons.visibility = View.GONE

            enableViews(inputPhoneNumber, fieldVerificationCode)
            inputPhoneNumber.text = null
            fieldVerificationCode.text = null

//            status.setText(R.string.signed_in)
//            detail.text = getString(R.string.firebase_status_fmt, user.uid)
        }
    }

    private fun validatePhoneNumber(): Boolean {
        val phoneNumber = inputPhoneNumber!!.text.toString()
        if (TextUtils.isEmpty(phoneNumber)) {
            inputPhoneNumber!!.error = "Invalid phone number."
            return false
        }

        return true
    }

    private fun enableViews(vararg views: View) {
        for (v in views) {
            v.isEnabled = true
        }
    }

    private fun disableViews(vararg views: View) {
        for (v in views) {
            v.isEnabled = false
        }
    }

    override fun onClick(view: View) {
        when (view.id) {
            R.id.buttonStartVerification -> {
                if (!validatePhoneNumber()) {
                    return
                }

                startPhoneNumberVerification(inputPhoneNumber!!.text.toString())
                progressBar!!.visibility = View.VISIBLE
            }
            R.id.buttonVerifyPhone -> {
                val code = fieldVerificationCode!!.text.toString()
                if (TextUtils.isEmpty(code)) {
                    fieldVerificationCode!!.error = "Cannot be empty."
                    return
                }

                verifyPhoneNumberWithCode(storedVerificationId, code)
                progressBar!!.visibility = View.VISIBLE
            }
            R.id.buttonResend -> {
                resendVerificationCode(inputPhoneNumber!!.text.toString(), resendToken)
                progressBar!!.visibility = View.VISIBLE
            }

            // R.id.signOutButton -> signOut()
        }
    }

    companion object {
        private const val TAG = "PhoneAuthActivity"
        private const val KEY_VERIFY_IN_PROGRESS = "key_verify_in_progress"
        private const val STATE_INITIALIZED = 1
        private const val STATE_VERIFY_FAILED = 3
        private const val STATE_VERIFY_SUCCESS = 4
        private const val STATE_CODE_SENT = 2
        private const val STATE_SIGNIN_FAILED = 5
        private const val STATE_SIGNIN_SUCCESS = 6
    }

}




//import androidx.appcompat.app.AppCompatActivity
//import android.os.Bundle
////
////class LoginRegisterActivity : AppCompatActivity() {
////
////    override fun onCreate(savedInstanceState: Bundle?) {
////        super.onCreate(savedInstanceState)
////        setContentView(R.layout.activity_login_register)
////    }
////}
//
//
//import android.content.Intent
//import android.widget.Toast
//import android.text.TextUtils
//import android.widget.ProgressBar
//import android.view.View
//import android.view.WindowManager
//import android.widget.Button
//import android.widget.EditText
//
//import com.google.firebase.auth.FirebaseAuth
//import com.google.firebase.auth.PhoneAuthCredential
//import com.google.firebase.auth.PhoneAuthProvider
//
//
//import com.google.android.gms.common.util.NumberUtils
//import java.util.*
//
//class LoginRegisterActivity : AppCompatActivity() {
//
//    private var inputFirstName: EditText? = null
//    private var inputLastName: EditText? = null
//    private var inputPhoneNumber: EditText? = null
//
//    private var inputEmail: EditText? = null
//    private var inputPassword: EditText? = null
//    private var auth: FirebaseAuth? = null
//    private var progressBar: ProgressBar? = null
//    private var btnSignup: Button? = null
//    private var btnLogin: Button? = null
//    private var btnReset: Button? = null
//
//    private var storedVerificationId: String? = null
//    private lateinit var resendToken: PhoneAuthProvider.ForceResendingToken
//
//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//
//        val w = window
//        w.setFlags(
//            WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
//            WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS
//        )
//
//        auth = FirebaseAuth.getInstance()
//        auth!!.setLanguageCode(Locale.ENGLISH.language)
//
//
//
//        if (auth!!.currentUser != null) {
//            startActivity(Intent(this@LoginRegisterActivity, MainActivity::class.java))
//            finish()
//        }
//
//        setContentView(R.layout.activity_login_register)
//
//        inputFirstName = findViewById<EditText>(R.id.firstName)
//        inputLastName = findViewById<EditText>(R.id.lastName)
//        inputPhoneNumber = findViewById<EditText>(R.id.phoneNumber)
//        inputEmail = findViewById<EditText>(R.id.email)
////        inputPassword = findViewById<EditText>(R.id.inputOldPassword)
//        progressBar = findViewById<ProgressBar>(R.id.progressBar)
//        btnSignup = findViewById<Button>(R.id.sign_up_button)
////        btnLogin = findViewById<Button>(R.id.btn_login)
////        btnReset = findViewById<Button>(R.id.btn_reset_password)
//
//        btnLogin!!.setOnClickListener { userLoginIn() }
//        btnSignup!!.setOnClickListener { userRegister() }
//        btnReset!!.setOnClickListener { userForgotPassword() }
//    }
//
//    private fun userLoginIn() {
////        val email = inputEmail!!.text.toString()
////        val password = inputPassword!!.text.toString()
//        val phoneNumber  = inputPhoneNumber!!.text.toString().toInt()
//        val firstName = inputFirstName!!.text.toString()
//        val lastName = inputLastName!!.text.toString()
//        val email = inputEmail!!.text.toString()
//
//        when {
//            TextUtils.isEmpty(email) -> inputEmail!!.error = "Enter email address!"
//            TextUtils.isEmpty(firstName) -> inputPhoneNumber!!.error = "Enter first name*"
//            TextUtils.isEmpty(firstName) -> inputPhoneNumber!!.error = "Enter last name*"
//            phoneNumber == null -> inputPhoneNumber!!.error = "Enter phone number*"
//
//            else -> {
////                val isUserSignedIn = FirebaseAuth.getInstance().currentUser != null
//
//                progressBar!!.visibility = View.VISIBLE
//
//
//
//                auth!!.signInWithEmailAndPassword(email, password)
//                    .addOnCompleteListener(
//                        this@LoginRegisterActivity
//                    ) { task ->
//                        progressBar!!.visibility = View.GONE
//                        if (!task.isSuccessful) {
//                            if (password.length < 6) {
//                                inputPassword!!.error = "Password too short, enter minimum 6 characters!"
//                            } else {
//                                inputPassword!!.error = "Authentication failed, Check your Email and Password or Sign Up"
//                            }
//                        } else {
//                            val intent = Intent(this@LoginRegisterActivity, MainActivity::class.java)
//                            startActivity(intent)
//                            finish()
//                        }
//                    }
//            }
//        }
//    }
//
//
//    private fun userRegister() {
//        val email = inputEmail!!.text.toString().trim { it <= ' ' }
////        val password = inputPassword!!.text.toString().trim { it <= ' ' }
//        val phoneNumber  = inputPhoneNumber!!.text.toString().toInt()
//        val firstName = inputFirstName!!.text.toString()
//        val lastName = inputLastName!!.text.toString()
////        val email = inputEmail!!.text.toString()
//
//        when {
//            TextUtils.isEmpty(email) -> inputEmail!!.error = "Enter email address!"
//
////            TextUtils.isEmpty(password) -> inputPassword!!.error = "Enter password!"
//
////            password.length < 6 -> inputPassword!!.error = "Password too short, enter minimum 6 characters!"
//            TextUtils.isEmpty(firstName) -> inputFirstName!!.error = "Enter your first name!"
//            TextUtils.isEmpty(lastName) -> inputLastName!!.error = "Enter your last name!"
//            TextUtils.isEmpty(phoneNumber.toString()) -> inputPhoneNumber!!.error = "Enter your phone number!"
//
//            else -> {
//                progressBar!!.visibility = View.VISIBLE
//
//                auth!!.createUserWithEmailAndPassword(email, password)
//                    .addOnCompleteListener(
//                        this@LoginRegisterActivity
//                    ) { task ->
//                        Toast.makeText(
//                            this@LoginRegisterActivity,
//                            "Account Created. Here you go to next activity." + task.isSuccessful,
//                            Toast.LENGTH_SHORT
//                        ).show()
//                        progressBar!!.visibility = View.GONE
//
//                        if (!task.isSuccessful) {
//                            Toast.makeText(
//                                this@LoginRegisterActivity, "Authentication failed." + task.exception!!,
//                                Toast.LENGTH_SHORT
//                            ).show()
//                        } else {
//                            startActivity(Intent(this@LoginRegisterActivity, MainActivity::class.java))
//                            finish()
//                        }
//                    }
//            }
//        }
//    }
//
//    private fun userForgotPassword() {
//        val email = inputEmail!!.text.toString().trim { it <= ' ' }
//
//        if (TextUtils.isEmpty(email)) {
//            inputEmail!!.error = "Enter email address!"
//        }
//
//        else {
//            progressBar!!.visibility = View.VISIBLE
//            auth!!.sendPasswordResetEmail(email)
//                .addOnCompleteListener { task ->
//                    if (task.isSuccessful) {
//                        Toast.makeText(
//                            this@LoginRegisterActivity,
//                            "We have sent you instructions to reset your password!",
//                            Toast.LENGTH_SHORT
//                        ).show()
//                    } else {
//                        Toast.makeText(
//                            this@LoginRegisterActivity,
//                            "Failed to send reset email!",
//                            Toast.LENGTH_SHORT
//                        ).show()
//                    }
//
//                    progressBar!!.visibility = View.GONE
//                }
//        }
//    }
//}
//
//
//private fun saveUser(first_name: String, last_name: String, email: String, phone: Int){
//
//
