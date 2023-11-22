package com.example.myapp

import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import com.google.android.material.bottomnavigation.BottomNavigationView
import io.socket.client.IO
import io.socket.client.Socket
import java.net.URISyntaxException
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        try {
            val socket = IO.socket("http://10.0.2.2:777")
            SocketManager.setSocket(socket)
            SocketManager.connect()
        } catch (e: URISyntaxException) {
            e.printStackTrace()
        }

        val bottomNavigationView = findViewById<BottomNavigationView>(R.id.bottom_navigation)
        NaviHelper.setupBottomNavigationView(bottomNavigationView, supportFragmentManager)

        // 기본으로 표시할 프래그먼트 설정
        if (savedInstanceState == null) { // 액티비티가 처음 생성될 때만 실행
            bottomNavigationView.selectedItemId = R.id.navigation_calendar
        }
    }
}
