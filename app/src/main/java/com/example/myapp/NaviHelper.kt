package com.example.myapp

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import com.google.android.material.bottomnavigation.BottomNavigationView

object NaviHelper {
    private var currentFragment: Fragment? = null

    fun setupBottomNavigationView(navView: BottomNavigationView, fragmentManager: FragmentManager) {
        navView.setOnItemSelectedListener { menuItem ->
            val newFragment = when (menuItem.itemId) {
                //탭에 대한 프리그먼트 지정
                R.id.navigation_calendar -> fragmentManager.findFragmentByTag("Calendar") ?: CalendarFragment()
                R.id.navigation_work_log -> fragmentManager.findFragmentByTag("WorkLog") ?: WorkLogFragment()
                R.id.navigation_search -> fragmentManager.findFragmentByTag("WorkSearch") ?: WorkSearchFragment()
                R.id.navigation_info -> fragmentManager.findFragmentByTag("Info") ?: InfoFragment()
                else -> return@setOnItemSelectedListener false
            }

            fragmentManager.beginTransaction().apply {
                // 현재 보이는 프래그먼트를 숨깁니다.
                currentFragment?.let { hide(it) }
                // 프래그먼트가 이미 추가되었으면 보여주고, 그렇지 않으면 추가합니다.
                if (!newFragment.isAdded) {
                    add(R.id.fragment_container, newFragment, newFragment.javaClass.simpleName)
                } else {
                    show(newFragment)
                }
                commit()
            }
            // 현재 프래그먼트를 업데이트합니다.
            currentFragment = newFragment
            true
        }
    }
}
