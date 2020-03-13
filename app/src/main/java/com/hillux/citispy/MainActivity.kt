package com.hillux.citispy

//import android.R
import android.content.Intent
import android.os.Bundle
import android.view.MenuItem
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.core.view.GravityCompat
import androidx.drawerlayout.widget.DrawerLayout
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
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

    private var mDrawer: DrawerLayout? = null
    private var toolbar: Toolbar? = null
    private var nvDrawer: NavigationView? = null


    val firebaseAuth = FirebaseAuth.getInstance()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        auth = FirebaseAuth.getInstance()
        user = FirebaseAuth.getInstance().currentUser

        toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar)
        // This will display an Up icon (<-), we will replace it with hamburger later
        supportActionBar?.setDisplayHomeAsUpEnabled(true);

        // Find our drawer view
        mDrawer = findViewById<DrawerLayout>(R.id.drawer_layout);

        nvDrawer = findViewById<NavigationView>(R.id.navView);
        // Setup drawer view
        setupDrawerContent(nvDrawer!!);

        // Lookup navigation view
        // Lookup navigation view
        val navigationView =
            findViewById<View>(R.id.navView) as NavigationView

        // There is usually only 1 header view.
        // Multiple header views can technically be added at runtime.
        // We can use navigationView.getHeaderCount() to determine the total number.
        if (navigationView.headerCount > 0) {
            // avoid NPE by first checking if there is at least one Header View available
            val headerLayout = navigationView.getHeaderView(0)
        }
    }
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // The action bar home/up action should open or close the drawer.
        when (item.getItemId()) {
            android.R.id.home -> {
                mDrawer!!.openDrawer(GravityCompat.START)
                return true
            }
        }
        return super.onOptionsItemSelected(item)
    }

    private fun setupDrawerContent(navigationView: NavigationView) {
        navigationView.setNavigationItemSelectedListener { menuItem ->
            selectDrawerItem(menuItem)
            true
        }
    }

    fun selectDrawerItem(menuItem: MenuItem) {
        // Create a new fragment and specify the fragment to show based on nav item clicked
        var fragment: Fragment? = null
        val fragmentClass: Class<*> = when (menuItem.itemId) {
            R.id.main_fragment -> RaiseAlarm::class.java
            R.id.tag_person_fragment -> TagUser::class.java
            R.id.edit_profile_fragment -> EditProfile::class.java
            else -> RaiseAlarm::class.java
        }
        try {
            fragment = fragmentClass.newInstance() as Fragment
        } catch (e: Exception) {
            e.printStackTrace()
        }

        // Insert the fragment by replacing any existing fragment
        val fragmentManager: FragmentManager = supportFragmentManager
        if (fragment != null) {
            fragmentManager.beginTransaction().replace(R.id.main_fragment, fragment).commit()
        }

        // Highlight the selected item has been done by NavigationView
        menuItem.isChecked = true
        // Set action bar title
        title = menuItem.title
        // Close the navigation drawer
        mDrawer!!.closeDrawers()
    }

//    override fun onStart() {
//        super.onStart()
//        firebaseAuth!!.addAuthStateListener (this.authStateListener);
//    }
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

