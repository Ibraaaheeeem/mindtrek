package com.haneef.medquiz.ui.home

import DateTimePickerDialogFragment
import MockSetup
import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.CheckBox
import android.widget.ImageButton
import android.widget.ImageView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.gson.Gson
import com.haneef.medquiz.Category
import com.haneef.medquiz.Item
import com.haneef.medquiz.MainActivity
import com.haneef.medquiz.MyAdapter
import com.haneef.medquiz.R
import com.haneef.medquiz.Subcategory
import com.haneef.medquiz.Subject
import com.haneef.medquiz.Unit
import com.haneef.medquiz.data.MockData
import com.haneef.medquiz.data.ResponseQuizData
import com.haneef.medquiz.databinding.ActivityMainBinding
import com.haneef.medquiz.databinding.FragmentHomeBinding
import com.haneef.medquiz.multilevelview.MultiLevelRecyclerView
import com.haneef.medquiz.multilevelview.models.RecyclerViewItem
import com.haneef.medquiz.network.NetworkHandler
import com.haneef.medquiz.utils.AlertUtils
import com.haneef.medquiz.utils.PrefsManager
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.Call
import okhttp3.Callback
import okhttp3.Response
import java.io.IOException
import java.util.Calendar
import java.util.Locale
import java.util.concurrent.TimeUnit


class HomeFragment : Fragment(), DateTimePickerDialogFragment.DateTimePickerListener, MyAdapter.FragmentNavigationListener {

    private var mockScheduleMillis: Long = 0
    private lateinit var scheduleNowButton: CheckBox
    private lateinit var freeStyleButton: ImageView
    private lateinit var mockStyleButton: ImageView
    private lateinit var startMockButton: ImageButton
    private lateinit var scheduleDateTimeButton: Button
    private var myAdapter: MyAdapter? = null
    private lateinit var multiLevelRecyclerView: MultiLevelRecyclerView
    private var _binding: FragmentHomeBinding? = null
    private val MOCK_STYLE_TEST = 9
    private val FREE_STYLE_TEST = 10
    private var testStyle = FREE_STYLE_TEST
    private lateinit var mockScheduleDate: String
    private val CREATE_MOCK_ENDPOINT="/attempt/mock"


    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        multiLevelRecyclerView = binding.multilevelRecycler
        multiLevelRecyclerView.layoutManager = LinearLayoutManager(requireContext())
        mockStyleButton = binding.imageMockStyle
        freeStyleButton = binding.imageFreeStyle
        startMockButton = binding.startMockButton
        scheduleDateTimeButton = binding.scheduleTime
        scheduleNowButton = binding.scheduleNow
        mockScheduleDate = ""
        scheduleDateTimeButton.setOnClickListener{
            showDateTimePickerDialog()
        }
        scheduleNowButton.setOnCheckedChangeListener{view, isChecked ->
            if (isChecked) {
                scheduleDateTimeButton.setText("Schedule Date/Time")
                mockScheduleDate = ""
            }
            else {
                if (mockScheduleDate == "")
                    scheduleDateTimeButton.setText("Schedule Date/Time")
                else
                    scheduleDateTimeButton.setText(mockScheduleDate)
            }

        }
        val root: View = binding.root

        readCategoriesFromBackend()
        (freeStyleButton.parent as View).setBackgroundColor(Color.MAGENTA)
        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
    private fun getCategories() {
        val categories = readCategoriesFromBackend()
        Log.d("CATS",categories.size.toString())
    }

    fun showDateTimePickerDialog() {
        val dateTimePickerDialog = DateTimePickerDialogFragment()
        dateTimePickerDialog.setListener(this)
        dateTimePickerDialog.show(requireFragmentManager(), "Schedule Mock Date and Time")
    }

    fun format2(number: Int): String {
        return String.format("%02d", number)
    }
    override fun onDateTimeSelected(day: Int, month: Int, year: Int, hour: Int, minuite: Int) {
        // Create a Calendar object representing the selected date and time
        val calendar = Calendar.getInstance()
        calendar.set(Calendar.YEAR, year)
        calendar.set(Calendar.MONTH, month) // Calendar months are 0-based
        calendar.set(Calendar.DAY_OF_MONTH, day)
        calendar.set(Calendar.HOUR_OF_DAY, hour)
        calendar.set(Calendar.MINUTE, minuite)
        calendar.set(Calendar.SECOND, 0)

        // Calculate the time in milliseconds from the current time
        val currentTimeMillis = System.currentTimeMillis()
        val selectedTimeMillis = calendar.timeInMillis

        // Calculate the time difference
        val timeDifferenceMillis = selectedTimeMillis - currentTimeMillis

        // Handle the selected date and time or time difference as needed
        // ...

        // Optionally, format the time difference for display
        val dateTime = "${format2(day)}-${format2(month)}-$year ${format2(hour)}:${format2(minuite)}:00"
        val formattedTimeDifference = formatTimeDifference(timeDifferenceMillis)

        val myScope = CoroutineScope(Dispatchers.Main)
        myScope.launch {
            scheduleDateTimeButton.setText(dateTime)
        }
        scheduleNowButton.isChecked = false
        mockScheduleDate = dateTime
        mockScheduleMillis = selectedTimeMillis
    }

    private fun formatTimeDifference(timeDifferenceMillis: Long): String {
        val hours = TimeUnit.MILLISECONDS.toHours(timeDifferenceMillis)
        val minutes = TimeUnit.MILLISECONDS.toMinutes(timeDifferenceMillis) % 60
        val seconds = TimeUnit.MILLISECONDS.toSeconds(timeDifferenceMillis) % 60
        return String.format("%02d:%02d:%02d", hours, minutes, seconds)
    }

    private fun readCategoriesFromBackend(): List<Category> {
        val myScope = CoroutineScope(Dispatchers.IO)
        var categoriesJson = ""
        var categoriesList = listOf<Category>()
        Log.d("CATS", "HERE")
        myScope.launch {

            val networkHandler = NetworkHandler(requireActivity(), false)
            categoriesJson = PrefsManager.getInstance(requireContext()).getCategoriesJson().toString()

            if (categoriesJson == "" || categoriesJson == null)
                categoriesJson = networkHandler.fetchWebPageContent("${resources.getString(R.string.root_url)}/quiz/get_all_categories")

            Log.d("CATS2", categoriesJson)
            if (categoriesJson != "" && categoriesJson != "ERROR") {

                categoriesList =
                    Gson().fromJson(categoriesJson, Array<Category>::class.java).toList()
                PrefsManager.getInstance(requireContext()).saveCategoriesJson(categoriesJson)
                withContext(Dispatchers.Main) {
                    hideLoadingLayout()
                    Log.d("CATS3", categoriesList.size.toString())
                    val itemList = recursivePopulateCategories(
                        categoriesList,
                        0,
                        categoriesList.size
                    ) as List<Item>
                    myAdapter = MyAdapter(
                        requireActivity(),
                        0,
                        itemList,
                        binding.mockSubjectsLayout,
                        binding.multilevelRecycler,
                        this@HomeFragment
                    )
                    multiLevelRecyclerView.adapter = myAdapter
                    multiLevelRecyclerView.setToggleItemOnClick(false)
                    multiLevelRecyclerView.setAccordion(false)
                    multiLevelRecyclerView.openTill(0, 1, 2, 3)
                    mockStyleButton.setOnClickListener {
                        if (PrefsManager.getInstance(requireContext()).getJwt() == null) {
                            findNavController().navigate(R.id.home_to_login)
                            return@setOnClickListener
                        }
                        testStyle = MOCK_STYLE_TEST
                        binding.mockLayout.visibility = View.VISIBLE
                        if (myAdapter != null) {
                            myAdapter!!.setTestStyle(MOCK_STYLE_TEST)
                            myAdapter!!.notifyDataSetChanged()
                                (freeStyleButton.parent as View).setBackgroundColor(Color.WHITE)
                                (mockStyleButton.parent as View).setBackgroundColor(Color.MAGENTA)
                        }
                        PrefsManager.getInstance(requireContext()).saveQuizMode("MOCK_MODE")
                        setupMockSelectButtons()
                    }

                    freeStyleButton.setOnClickListener {
                        testStyle = FREE_STYLE_TEST
                        binding.mockLayout.visibility = View.GONE
                        if (myAdapter != null) {
                            myAdapter!!.setTestStyle(FREE_STYLE_TEST)
                            myAdapter!!.notifyDataSetChanged()
                            (mockStyleButton.parent as View).setBackgroundColor(Color.WHITE)
                            (freeStyleButton.parent as View).setBackgroundColor(Color.MAGENTA)

                        }
                        PrefsManager.getInstance(requireContext()).saveQuizMode("FREE_MODE")
                    }

                    startMockButton.setOnClickListener {
                        showLoadingLayout()
                        val time = (binding.hourValue.text.toString()
                            .toInt() * 3600) + (binding.minuiteValue.text.toString()
                            .toInt() * 60) + binding.secondsValue.text.toString().toInt()
                        val subjects = myAdapter?.getMock()!!.subjects;
                        for (subject in subjects){
                            if (subject.num_questions == 0){
                                val alert = AlertUtils(requireContext())
                                alert.showAlert("Invalid selection", "No question count selected for ${subject.name}")
                                return@setOnClickListener
                            }
                        }

                        if (time == 0) {
                            val alert = AlertUtils(requireContext())
                            alert.showAlert("Invalid time", "Select valid time for quiz")
                            return@setOnClickListener
                        }
                        val mockData =
                            MockData(myAdapter?.getMock()!!.subjects, time, mockScheduleDate)
                        val callback = object : Callback {
                            override fun onResponse(call: Call, response: Response) {
                                // Handle the response here
                                val responseBody = response.body?.string()
                                Log.d("MOCKREG", responseBody.toString())
                                val gson = Gson()

                                val response = gson.fromJson(
                                    responseBody.toString(),
                                    ResponseQuizData::class.java
                                )
                                val myScope = CoroutineScope(Dispatchers.Main)
                                myScope.launch {
                                    hideLoadingLayout()
                                }
                                val message = response.msg
                                if (message == "Mock created") {
                                    val quizDataHolder = response.quiz_data.toMutableList()
                                    for( subject in response.quiz_data){
                                        if (subject.ids.size == 0){
                                            val alertUtils =
                                                AlertUtils(requireContext()) // 'this' is the context of your activity or fragment
                                            // Display an alert
                                            val myScope = CoroutineScope(Dispatchers.Main)
                                            myScope.launch {
                                                alertUtils.showAlert(
                                                    "Invalid selection",
                                                    "No question found for selection ${subject.subject}. Please, remove it.",
                                                    "OK"
                                                ) {

                                                }
                                            }
                                            return
                                        }
                                    }
                                    response.quiz_data = quizDataHolder
                                    if (response.quiz_data.size == 0) {

                                    }
                                    PrefsManager.getInstance(requireContext())
                                        .saveQuizData(responseBody.toString())
                                    //Log.d("MOCK DATA", PrefsManager.getInstance(requireContext()).getQuizData().toString())
                                    if (mockScheduleDate == "") {
                                        val myScope = CoroutineScope(Dispatchers.Main)
                                        myScope.launch {
                                            findNavController().navigate(R.id.home_to_quiz)
                                        }
                                    } else {
                                        saveQuizForDate(mockScheduleDate)
                                        val alertUtils =
                                            AlertUtils(requireContext()) // 'this' is the context of your activity or fragment
                                        // Display an alert
                                        val myScope = CoroutineScope(Dispatchers.Main)
                                        myScope.launch {
                                            alertUtils.showAlert(
                                                "Mock has been scheduled. You will be alerted to start 5 minuites to the time",
                                                "You have created your mock",
                                                "OK"
                                            ) {

                                            }
                                        }
                                    }
                                }
                                else if (response.msg == "Token has expired"){
                                    val alertUtils =
                                        AlertUtils(requireContext())
                                    val myScope = CoroutineScope(Dispatchers.Main)
                                    myScope.launch {
                                        alertUtils.showAlert(
                                            "Login again",
                                            "Your login details have expired. You are required to login again",
                                            "OK"
                                        ) {
                                            findNavController().navigate(R.id.home_to_login)
                                        }
                                    }
                                }
                                Log.d("USERREG", "message")
                            }

                            override fun onFailure(call: Call, e: IOException) {
                                Log.d("USERREG", e.message.toString())
                                // Handle any network or request errors here
                            }
                        }
                        val mockSetup = MockSetup(
                            "${resources.getString(R.string.root_url)}${CREATE_MOCK_ENDPOINT}",
                            PrefsManager.getInstance(requireContext()).getJwt().toString()
                        )
                        mockSetup.createMock(mockData, callback)

                    }
                }
            }
        }

        return categoriesList
    }

    private fun hideLoadingLayout() {
        val activityBinding: ActivityMainBinding? =
            (requireActivity() as MainActivity).getBinding()
        activityBinding!!.appBarMain.loadingLayout.visibility = View.GONE

    }
    private fun showLoadingLayout() {
        val activityBinding: ActivityMainBinding? =
            (requireActivity() as MainActivity).getBinding()
        activityBinding!!.appBarMain.loadingLayout.visibility = View.VISIBLE

    }

    private fun setupMockSelectButtons() {

        binding.hourUp.setOnClickListener{
            var hh = binding.hourValue.text.toString().toInt()
            if (hh == 99) binding.hourValue.setText("00")
            else binding.hourValue.setText(format2(binding.hourValue.text.toString().toInt() + 1))
        }

        binding.hourDown.setOnClickListener{
            var hh = binding.hourValue.text.toString().toInt()
            if (hh == 0) return@setOnClickListener
            else binding.hourValue.setText(format2(binding.hourValue.text.toString().toInt() - 1))
        }

        binding.minuiteUp.setOnClickListener{
            var mm = binding.minuiteValue.text.toString().toInt()
            if (mm == 59) binding.minuiteValue.setText("00")
            else binding.minuiteValue.setText(format2(binding.minuiteValue.text.toString().toInt() + 1))
        }

        binding.minuiteDown.setOnClickListener{
            var mm = binding.minuiteValue.text.toString().toInt()
            if (mm == 0) return@setOnClickListener
            else binding.minuiteValue.setText(format2(binding.minuiteValue.text.toString().toInt() - 1))
        }

        binding.secondsUp.setOnClickListener{
            var ss = binding.secondsValue.text.toString().toInt()
            if (ss == 59) binding.secondsValue.setText("00")
            else binding.secondsValue.setText(format2(binding.secondsValue.text.toString().toInt() + 1))
        }

        binding.secondsDown.setOnClickListener{
            var ss = binding.secondsValue.text.toString().toInt()
            if (ss == 0) return@setOnClickListener
            else binding.secondsValue.setText(format2(binding.secondsValue.text.toString().toInt() - 1))
        }
    }

    private fun saveQuizForDate(mockScheduleDate: String) {
        val alarmManager = context?.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val intent = Intent(requireActivity(), MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(requireActivity(), 0, intent, PendingIntent.FLAG_UPDATE_CURRENT)

        //val chosenTimeInMillis = System.currentTimeMillis() + (30 * 60 * 1000)

        alarmManager.set(AlarmManager.RTC_WAKEUP, mockScheduleMillis, pendingIntent)

    }

    private fun recursivePopulateCategories(itemsList: List<Any>, levelNumber: Int, depth: Int): List<*>? {
        val displayList: MutableList<RecyclerViewItem> = ArrayList()
        for (i in 0 until depth) {
            val objectToItem = when (levelNumber) {
                0 -> {
                    val category = itemsList[i] as Category
                    val item = Item(levelNumber).apply {
                        id = category.id
                        text = String.format(Locale.ENGLISH, category.name, i)
                        secondText = String.format(Locale.ENGLISH, category.nquestions.toString() + " questions", i)
                    }
                    if (category.subcategories.size > 0){
                        item.addChildren(
                            recursivePopulateCategories(
                                category.subcategories,
                                levelNumber + 1,
                                category.subcategories.size
                            ) as List<RecyclerViewItem?>?
                        )
                    }
                    item
                }
                1 -> {
                    val subcategory = itemsList[i] as Subcategory
                    val item = Item(levelNumber).apply {
                        id = subcategory.id
                        text = String.format(Locale.ENGLISH, subcategory.name, i)
                        secondText = String.format(Locale.ENGLISH, subcategory.nquestions.toString() + " questions", i)
                    }
                    if (subcategory.subjects.size > 0){
                        item.addChildren(
                            recursivePopulateCategories(
                                subcategory.subjects,
                                levelNumber + 1,
                                subcategory.subjects.size
                            ) as List<RecyclerViewItem?>?
                        )
                    }
                    item
                }
                2 -> {
                    val subject = itemsList[i] as Subject
                    val item = Item(levelNumber).apply {
                        id = subject.id
                        text = String.format(Locale.ENGLISH, subject.name, i)
                        secondText = String.format(Locale.ENGLISH, subject.nquestions.toString() + " questions", i)
                    }
                    if (subject.units.size > 0){
                        item.addChildren(
                            recursivePopulateCategories(
                                subject.units,
                                levelNumber + 1,
                                subject.units.size
                            ) as List<RecyclerViewItem?>?
                        )
                    }
                    item
                }
                3 -> {
                    val unit = itemsList[i] as Unit
                    val item = Item(levelNumber).apply {
                        id = unit.id
                        text = String.format(Locale.ENGLISH, unit.name, i)
                        if (unit.tags != null) secondText = String.format(Locale.ENGLISH, unit.nquestions.toString() + " questions", i)
                    }
                    if (unit.tags != null && unit.tags.size > 0){
                        item.addChildren(
                            recursivePopulateCategories(
                                unit.tags,
                                levelNumber + 1,
                                unit.tags.size
                            ) as List<RecyclerViewItem?>?
                        )
                    }
                    item
                }
                else -> {
                    val unit = itemsList[i] as String
                    Item(levelNumber).apply {
                        id = 0
                        text = String.format(Locale.ENGLISH, unit, i)
                        secondText = String.format(Locale.ENGLISH, " questions", i)
                    }
                }
            }
            displayList.add(objectToItem)
        }
        return displayList
    }

    override fun navigateToFragment(fragmentId: Int, bundle: Bundle) {
        findNavController().navigate(fragmentId, bundle)
    }

}