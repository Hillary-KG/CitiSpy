package com.hillux.citispy

import android.app.ListActivity
import android.app.SearchManager
import android.content.Intent
import android.os.Bundle

class SearchUserActivity: ListActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.tag_user_fragment)

        // Verify the action and get the query
        if (Intent.ACTION_SEARCH == intent.action) {
            intent.getStringExtra(SearchManager.QUERY)?.also { query ->
                doMySearch(query)
            }
        }
    }

    fun doMySearch(query:String){

    }
}