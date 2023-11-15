package com.example.myapp

import android.os.AsyncTask
import android.os.Bundle
import android.os.Environment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ListView
import androidx.fragment.app.Fragment
import java.io.BufferedReader
import java.io.File
import java.io.FileReader

class WorkSearchFragment : Fragment() {

    private lateinit var logListView: ListView
    private lateinit var adapter: ArrayAdapter<String>

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        // 프래그먼트 레이아웃을 인플레이트합니다.
        return inflater.inflate(R.layout.fragment_work_search, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        logListView = view.findViewById(R.id.logListView)
        adapter = ArrayAdapter(requireContext(), android.R.layout.simple_list_item_1)
        logListView.adapter = adapter

        LoadAndSortLogsTask().execute()
    }

    // LoadAndSortLogsTask AsyncTask 클래스와 다른 메소드들...
    private inner class LoadAndSortLogsTask : AsyncTask<Unit, Unit, List<String>>() {
        override fun doInBackground(vararg params: Unit?): List<String> {
            val logs = mutableListOf<String>()
            val fileName = "work_log.txt"
            val directory = requireActivity().getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS)
            val file = File(directory, fileName)

            if (file.exists()) {
                try {
                    val allLines = BufferedReader(FileReader(file)).readLines()
                    for (i in 0 until allLines.size step 4) {
                        if (i + 3 < allLines.size) {
                            val log = "${allLines[i]}\n${allLines[i + 1]}\n${allLines[i + 2]}\n${allLines[i + 3]}"
                            logs.add(log)
                        }
                    }

                    // Sort data by date
                    logs.sortBy { extractDate(it) }
                } catch (e: Exception) {
                    e.printStackTrace()
                    // Here you can also add a Toast to inform the user about the error
                }
            }

            return logs
        }

        override fun onPostExecute(result: List<String>?) {
            result?.let {
                adapter.clear()
                adapter.addAll(result)
                adapter.notifyDataSetChanged()
            }
        }
    }

    private fun extractDate(line: String): String? {
        val pattern = "Date: (\\d{4}-\\d{2}-\\d{2})"
        val regex = Regex(pattern)
        val matchResult = regex.find(line)
        return matchResult?.groupValues?.getOrNull(1)
    }

    private fun extractCompany(line: String): String? {
        val pattern = "Company: (.+)"
        val regex = Regex(pattern)
        val matchResult = regex.find(line)
        return matchResult?.groupValues?.getOrNull(2)
    }

    private fun extractSite(line: String): String? {
        val pattern = "Site: (.+)"
        val regex = Regex(pattern)
        val matchResult = regex.find(line)
        return matchResult?.groupValues?.getOrNull(3)
    }
}
