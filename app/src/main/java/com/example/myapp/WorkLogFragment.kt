package com.example.myapp

import android.app.DatePickerDialog
import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.InputMethodManager
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import java.io.File
import java.io.FileOutputStream
import java.util.*
import android.Manifest
import android.os.Environment
import org.json.JSONObject
import java.net.Socket

class WorkLogFragment : Fragment() {
    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // 프래그먼트 레이아웃을 인플레이트합니다.
        return inflater.inflate(R.layout.fragment_work_log, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // 여기에 UI 컴포넌트 초기화 및 이벤트 리스너 설정
        var workDateInput: TextView = view.findViewById(R.id.work_date_input)
        var workCompanyInput: EditText = view.findViewById(R.id.work_company_input)
        var workSiteInput: EditText = view.findViewById(R.id.work_site_input)
        val resetButton: Button = view.findViewById(R.id.reset)
        val writeButton: Button = view.findViewById(R.id.write)
        val layout: LinearLayout = view.findViewById(R.id.layout)

        // 날짜 선택 다이얼로그 설정
        workDateInput.setOnClickListener {
            val calendar = Calendar.getInstance()
            DatePickerDialog(requireContext(), { _, year, month, dayOfMonth ->
                val selectedDate = "$year-${month + 1}-$dayOfMonth"
                workDateInput.text = selectedDate
            }, calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH)).show()
        }

        // 리셋 버튼 이벤트
        resetButton.setOnClickListener {
            workCompanyInput.text.clear()
            workSiteInput.text.clear()
            workDateInput.text = ""
        }

        // 작성 버튼 이벤트
        writeButton.setOnClickListener {
            val date = workDateInput.text.toString()
            val company = workCompanyInput.text.toString()
            val site = workSiteInput.text.toString()
            if(date.isNotEmpty() && company.isNotEmpty() && site.isNotEmpty()){
                val jsonData = JSONObject().apply {
                    put("date", date)
                    put("company", company)
                    put("site", site)
                }
                SocketManager.getSocket()?.emit("EventName", jsonData)
                Log.d("WorkLogFragment", "push") // 'YourFragment'는 로그 태그, 'push'는 로그 메시지입니다.
            }
            else{
                //데이터가 비어있을경우 발생 코드추가 예정
            }
            saveDataToFile("Date: $date\nCompany: $company\nSite: $site")
        }

        // 키보드 숨기기
        layout.setOnTouchListener { _, _ ->
            hideKeyboard()
            false
        }
    }

    private fun hideKeyboard() {
        val inputMethodManager = context?.getSystemService(Context.INPUT_METHOD_SERVICE) as? InputMethodManager
        inputMethodManager?.hideSoftInputFromWindow(view?.windowToken, 0)
    }

    private fun saveDataToFile(data: String) {
        try {
            val fileName = "work_log.txt"
            //val directory = context?.getExternalFilesDir(null)
            val directory = requireActivity().getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS)

            if (directory != null) {
                val file = File(directory, fileName)
                FileOutputStream(file, true).use { outputStream ->
                    outputStream.write(data.toByteArray())
                    outputStream.write("\n\n".toByteArray()) // 데이터 구분을 위한 줄바꿈 추가
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}