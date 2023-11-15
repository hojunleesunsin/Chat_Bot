package com.example.myapp

import android.app.AlertDialog
import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class CalendarAdapter(
    private val context: Context,
    private var daysOfWeek: Array<String>,
    private var days: List<String>,
    private var events: MutableList<MutableList<String>>,
    private val onEventChanged: () -> Unit  // 콜백 추가
) : RecyclerView.Adapter<CalendarAdapter.ViewHolder>() {

    private val inflater: LayoutInflater = LayoutInflater.from(context)

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val dayText: TextView = view.findViewById(R.id.day_text)
        val eventText: TextView = view.findViewById(R.id.event_text)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = inflater.inflate(R.layout.item_calendar, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        if (position < 7) {
            holder.dayText.text = daysOfWeek[position]
            holder.eventText.visibility = View.GONE
            holder.itemView.isClickable = false
        } else {
            val actualPosition = position - 7
            if (actualPosition in days.indices) {
                holder.dayText.text = days[actualPosition]
                holder.eventText.text = events[actualPosition].joinToString(", ")

                holder.itemView.setOnClickListener {
                    val builder = AlertDialog.Builder(context)
                    builder.setTitle("${days[actualPosition]}일의 일정")

                    val eventInput = EditText(context)
                    builder.setView(eventInput)

                    val eventList = events[actualPosition].toTypedArray()
                    builder.setSingleChoiceItems(eventList, -1) { dialog, which ->
                        eventInput.setText(eventList[which])
                    }

                    builder.setPositiveButton("저장") { _, _ ->
                        val event = eventInput.text.toString()
                        if (event.isNotEmpty()) {
                            events[actualPosition].add(event)
                            notifyItemChanged(position)
                            onEventChanged()  // 콜백 호출
                        }
                    }

                    builder.setNegativeButton("삭제") { _, _ ->
                        val event = eventInput.text.toString()
                        events[actualPosition].remove(event)
                        notifyItemChanged(position)
                        onEventChanged()  // 콜백 호출
                    }

                    builder.setNeutralButton("취소") { dialog, _ -> dialog.cancel() }

                    builder.show()
                }
            }
        }
    }

    fun updateData(daysOfWeek: Array<String>, days: List<String>, events: MutableList<MutableList<String>>) {
        this.daysOfWeek = daysOfWeek
        this.days = days
        this.events = events
        notifyDataSetChanged()
    }

    override fun getItemCount(): Int {
        return days.size + 7
    }


}