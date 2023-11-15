package com.example.myapp

import android.app.DatePickerDialog
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.util.*

class CalendarFragment : Fragment() {

    private val eventsMap = mutableMapOf<String, MutableList<MutableList<String>>>()
    private val daysOfWeek = arrayOf("일", "월", "화", "수", "목", "금", "토")

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // 프래그먼트의 레이아웃을 반환합니다.
        return inflater.inflate(R.layout.fragment_calendar, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        loadEvents()

        val currentDate = Calendar.getInstance()
        val year = currentDate.get(Calendar.YEAR)
        val month = currentDate.get(Calendar.MONTH) + 1

        val dateText: TextView = view.findViewById(R.id.date_text)
        val recyclerView: RecyclerView = view.findViewById(R.id.recycler_view)

        recyclerView.layoutManager = GridLayoutManager(context, 7)
        recyclerView.addItemDecoration(SpaceItemDecoration(100, 7))
        recyclerView.adapter = CalendarAdapter(requireContext(), daysOfWeek, listOf(), MutableList(7) { mutableListOf<String>() }) {
            saveEvents()  // 이벤트 변경 시 saveEvents 함수를 호출
        }
        updateCalendar(currentDate, dateText, year, month)

        // Open a DatePickerDialog when dateText is clicked
        dateText.setOnClickListener {
            DatePickerDialog(requireContext(), { _, selectedYear, selectedMonth, _ ->
                updateCalendar(currentDate, dateText, selectedYear, selectedMonth + 1)
            }, year, month - 1, 1).show()
        }
    }

    // MainActivity에서 사용된 기타 메소드들을 여기로 이동 및 수정
    // 예: updateCalendar, saveEvents, loadEvents
    private fun updateCalendar(currentDate: Calendar, dateText: TextView, year: Int, month: Int) {
        currentDate.set(Calendar.YEAR, year)
        currentDate.set(Calendar.MONTH, month - 1)
        dateText.text = "$year 년 $month 월"

        val key = "$year-$month"
        val daysInMonth = currentDate.getActualMaximum(Calendar.DAY_OF_MONTH)
        val days = List(daysInMonth) { (it + 1).toString() }
        currentDate.set(Calendar.DAY_OF_MONTH, 1)
        val firstDayOfWeek = currentDate.get(Calendar.DAY_OF_WEEK)
        val offsetDays = List(firstDayOfWeek - 1) { "" }
        val combinedDays = offsetDays + days
        val events =
            eventsMap.getOrPut(key) { MutableList(combinedDays.size) { mutableListOf<String>() } }
        val recyclerView: RecyclerView? = view?.findViewById(R.id.recycler_view)
        (recyclerView?.adapter as CalendarAdapter).updateData(daysOfWeek, combinedDays, events)
    }

    private fun saveEvents() {
        val sharedPreferences = requireActivity().getSharedPreferences("calendar_events",
            AppCompatActivity.MODE_PRIVATE
        )
        val editor = sharedPreferences.edit()
        val gson = Gson()  // Gson 라이브러리를 사용하여 객체를 문자열로 변환
        val json = gson.toJson(eventsMap)
        editor.putString("events_data", json)
        editor.apply()
    }

    private fun loadEvents() {
        val sharedPreferences = requireActivity().getSharedPreferences("calendar_events",
            AppCompatActivity.MODE_PRIVATE
        )
        val gson = Gson()
        val json = sharedPreferences.getString("events_data", null)
        val type = object : TypeToken<MutableMap<String, MutableList<MutableList<String>>>>() {}.type
        val loadedData = gson.fromJson<MutableMap<String, MutableList<MutableList<String>>>>(json, type)
        if (loadedData != null) {
            eventsMap.clear()
            eventsMap.putAll(loadedData)
        }
    }
}
