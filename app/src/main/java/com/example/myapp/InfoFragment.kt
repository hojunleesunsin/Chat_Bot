package com.example.myapp

import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.fragment.app.Fragment
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity

class InfoFragment : Fragment() {
    // 선언
    private lateinit var profileImageView: ImageView
    private lateinit var selectImageButton: Button
    private lateinit var deleteImageButton: Button
    private lateinit var nameEditText: EditText
    private lateinit var companyEditText: EditText
    private lateinit var emailEditText: EditText
    private lateinit var faxEditText: EditText
    private lateinit var phoneEditText: EditText
    private lateinit var addressEditText: EditText
    private lateinit var carTypeEditText: EditText
    private lateinit var carNumberEditText: EditText

    private val telecomOptions = arrayOf("SKT", "KT", "LG U+", "SKT 알뜰폰", "KT 알뜰폰", "LG U+ 알뜰폰")

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        return inflater.inflate(R.layout.fragment_info, container, false)
    }

    // static
    companion object {
        private const val IMAGE_PICK_REQUEST = 1
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // UI 컴포넌트 초기화
        profileImageView = view.findViewById(R.id.profileImageView)
        selectImageButton = view.findViewById(R.id.selectImageButton)
        deleteImageButton = view.findViewById(R.id.deleteImageButton)
        nameEditText = view.findViewById(R.id.nameEditText)
        companyEditText = view.findViewById(R.id.companyEditText)
        emailEditText = view.findViewById(R.id.emailEditText)
        faxEditText = view.findViewById(R.id.faxEditText)
        phoneEditText = view.findViewById(R.id.phoneEditText)
        addressEditText = view.findViewById(R.id.addressEditText)
        carTypeEditText = view.findViewById(R.id.carTypeEditText)
        carNumberEditText = view.findViewById(R.id.carNumberEditText)

        selectImageButton.setOnClickListener {
            // 갤러리에서 이미지 선택
            val intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
            imagePickLauncher.launch(intent)
        }

        deleteImageButton.setOnClickListener {
            // 프로필 이미지 삭제 (기본 이미지로 설정)
            profileImageView.setImageResource(R.drawable.default_profile_image)
        }

        addressEditText.setOnClickListener {
            //주소 검색 웹뷰 화면 이동
            val intent = Intent(requireContext(), SearchActivity::class.java)
            getSearchResult.launch(intent)
        }
        //통신사 스피너 선택
        val telecomSpinner: Spinner = view.findViewById(R.id.telecomSpinner)
        val telecomAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, telecomOptions)
        telecomAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        telecomSpinner.adapter = telecomAdapter

    }

    private val getSearchResult = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == AppCompatActivity.RESULT_OK) {
            result.data?.let { data ->
                val address = data.getStringExtra("data")
                addressEditText.setText(address)
            }
        }
    }

    // 이미지 선택 결과 처리
    private val imagePickLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == android.app.Activity.RESULT_OK && result.data != null) {
            try {
                val bitmap: Bitmap = MediaStore.Images.Media.getBitmap(requireActivity().contentResolver, result.data!!.data)
                profileImageView.setImageBitmap(bitmap)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
