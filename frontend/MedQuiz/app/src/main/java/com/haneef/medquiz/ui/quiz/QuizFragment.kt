package com.haneef.medquiz.ui.quiz

import TimerUtils
import UrlFetchService
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.CompoundButton
import android.widget.RadioGroup
import android.widget.RadioGroup.OnCheckedChangeListener
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.google.gson.Gson
import com.haneef.medquiz.R
import com.haneef.medquiz.data.BackendResponse
import com.haneef.medquiz.data.Question
import com.haneef.medquiz.data.QuizData
import com.haneef.medquiz.data.QuizEndData
import com.haneef.medquiz.data.QuizEndSubject
import com.haneef.medquiz.data.QuizRunning
import com.haneef.medquiz.data.ResponseQuestions
import com.haneef.medquiz.data.ResponseQuizData
import com.haneef.medquiz.databinding.FragmentQuizBinding
import com.haneef.medquiz.utils.AlertUtils
import com.haneef.medquiz.utils.PrefsManager
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.Call
import okhttp3.Callback
import okhttp3.Response
import java.io.IOException


open class QuizFragment : Fragment(), TimerUtils.TimerCallback {

    private lateinit var currentQuestion: Question
    private var quizMode: String? = null
    private lateinit var runningQuiz: QuizRunning
    private var _binding: FragmentQuizBinding? = null
    private var quizData: QuizData? = null
    private val categoryLevel = 0
    private val levelId = 0
    private val GET_QUESTIONS_ENPOINT = "/quiz/questions"
    private val GET_QUESTION_ENPOINT = "/quiz/question"
    private lateinit var optionsRadioGroup: RadioGroup
    private lateinit var myQuizData: ResponseQuizData
    private var currentSubjectIndex = 0
    private var currentQuestionIndex = 0

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private fun getUrlComposed(): String{
        return "${GET_QUESTION_ENPOINT}/${categoryLevel}/${levelId}?n=1"
    }
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentQuizBinding.inflate(inflater, container, false)
        quizMode = PrefsManager.getInstance(requireContext()).getQuizMode()
        when (quizMode){
            "MOCK_MODE" -> {
                val storedQuizData = PrefsManager.getInstance(requireContext()).getQuizData()
                if (storedQuizData == null){
                    val alertUtils = AlertUtils(requireContext())
                    alertUtils.showAlert("No quiz data", "No quiz data found. Return to select quiz data", "YES"){
                        findNavController().navigate(R.id.quiz_to_home)
                    }
                }
                Log.d("INSIDE", "QUIZ_MODE")
                myQuizData = Gson().fromJson(storedQuizData, ResponseQuizData::class.java)
                Log.d("INSIDE", storedQuizData.toString())

                setUpQuiz(myQuizData)
            }
            "FREE_MODE" -> {
                val bundle = arguments
                if (bundle != null) {
                    val subjectId = bundle.getInt("subject_id")
                    val subjectName = bundle.getString("subject_name")
                    val level = bundle.getInt("subject_level")
                    setUpFreeMode(subjectName.toString(), subjectId, level)
                }
            }
        }
        val root: View = binding.root
        return root
    }

    private fun setUpFreeMode(subjectName: String, subjectId: Int, level: Int) {
        binding.previousQuestionButton.visibility = View.GONE
        binding.explanationLayout.visibility = View.GONE
        val questionUrl = "${resources.getString(R.string.root_url)}${GET_QUESTIONS_ENPOINT}/level/$level/category/$subjectId"
        val getQuestionService = UrlFetchService(questionUrl)
        val callback = object : Callback {
            override fun onResponse(call: Call, response: Response) {
                // Handle the response here
                val responseBody = response.body?.string()
                Log.d("GET QUESTION", responseBody.toString())
                val responseQuestion = Gson().fromJson(responseBody.toString(), ResponseQuestions::class.java)
                var myScope = CoroutineScope(Dispatchers.Main);
                if (responseQuestion.questions.size <= 0 ) {
                    var myScope = CoroutineScope(Dispatchers.Main);
                    myScope.launch {
                        val alertUtils = AlertUtils(requireContext())
                        alertUtils.showAlert("No question", "We couldn't find any question in this subject", "O.K."){
                            findNavController().navigate(R.id.quiz_to_home)
                        }
                    }
                    return
                }
                currentQuestion = responseQuestion.questions[0]
                myScope.launch { updateQuestionDataView(0, subjectName, responseQuestion.questions[0], 0) }
            }

            override fun onFailure(call: Call, e: IOException) {
                Log.d("USERREG", e.message.toString())
                // Handle any network or request errors here
            }
        }

        getQuestionService.fetchUrl("GET","", callback)
        binding.optionA.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionA.isChecked = true
                if (currentQuestion.correct_options[0] == 'A'){
                    binding.optionA.setBackgroundColor(Color.GREEN)
                }
                else{
                    binding.optionA.setBackgroundColor(Color.RED)
                    markCorrectAnswer(currentQuestion.correct_options[0])
                }
                showExplanation()
            }
        })
        binding.optionB.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionB.isChecked = true

                if (currentQuestion.correct_options[0] == 'B') {
                    binding.optionB.setBackgroundColor(Color.GREEN)
                }
                else {
                    binding.optionB.setBackgroundColor(Color.RED)
                    markCorrectAnswer(currentQuestion.correct_options[0])
                }
                showExplanation()
            }
        })
        binding.optionC.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionC.isChecked = true

                if (currentQuestion.correct_options[0] == 'C'){
                    binding.optionC.setBackgroundColor(Color.GREEN)
                }
                else{
                    binding.optionC.setBackgroundColor(Color.RED)
                    markCorrectAnswer(currentQuestion.correct_options[0])
                }
                showExplanation()
            }
        })
        binding.optionD.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionD.isChecked = true

                if (currentQuestion.correct_options[0] == 'D'){
                    binding.optionD.setBackgroundColor(Color.GREEN)
                }
                else{
                    binding.optionD.setBackgroundColor(Color.RED)
                    markCorrectAnswer(currentQuestion.correct_options[0])
                }
                showExplanation()
            }
        })
        binding.optionE.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionE.isChecked = true

                if (currentQuestion.correct_options[0] == 'E'){
                    binding.optionE.setBackgroundColor(Color.GREEN)
                }
                else{
                    binding.optionE.setBackgroundColor(Color.RED)
                    markCorrectAnswer(currentQuestion.correct_options[0])
                }
                showExplanation()
            }
        })
        binding.nextQuestionButton.setOnClickListener{
            setUpFreeMode(subjectName, subjectId, level)
        }
    }

    private fun showExplanation() {
        binding.explanationLayout.visibility = View.VISIBLE
        binding.explanationText.setText((currentQuestion.explanation))
    }

    private fun markCorrectAnswer(correctAnswer: Char) {
        when(correctAnswer){
            'A' -> binding.optionA.setBackgroundColor(Color.GREEN)
            'B' -> binding.optionB.setBackgroundColor(Color.GREEN)
            'C' -> binding.optionC.setBackgroundColor(Color.GREEN)
            'D' -> binding.optionD.setBackgroundColor(Color.GREEN)
            'E' -> binding.optionE.setBackgroundColor(Color.GREEN)
        }
    }

    private fun setUpQuiz(myQuizData: ResponseQuizData?) {
        binding.optionA.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionA.isChecked = true
                runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'A'
            }
        })
        binding.optionB.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionB.isChecked = true
                runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'B'
            }
        })
        binding.optionC.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionC.isChecked = true
                runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'C'
            }
        })
        binding.optionD.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionD.isChecked = true
                runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'D'
            }
        })
        binding.optionE.setOnCheckedChangeListener(CompoundButton.OnCheckedChangeListener { buttonView, isChecked ->
            if (isChecked) {
                clearSelection()
                binding.optionE.isChecked = true
                runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'E'
            }
        })
        optionsRadioGroup = binding.optionsRadioGroup
        optionsRadioGroup.setOnCheckedChangeListener(object : OnCheckedChangeListener{
            override fun onCheckedChanged(group: RadioGroup?, checkedId: Int) {

                when (checkedId){
                    R.id.option_a -> {
                        if (binding.optionA.isChecked)
                            runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'A'
                    }
                    R.id.option_b -> {
                        if (binding.optionB.isChecked)
                            runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'B'
                    }
                    R.id.option_c -> {
                        if (binding.optionC.isChecked)
                            runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'C'
                    }
                    R.id.option_d -> {
                        if (binding.optionD.isChecked)
                            runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'D'
                    }

                    R.id.option_e -> {
                        if (binding.optionE.isChecked)
                            runningQuiz.answers[currentSubjectIndex][currentQuestionIndex] = 'E'
                    }
                }
                Log.d("SELECTED OPTION", runningQuiz.answers[currentSubjectIndex][currentQuestionIndex]+"")
            }
        })
        binding.submitQuizButton.setOnClickListener{
            markAnswers()
        }
        Log.d("GET QUESTION", "")
        initializeRunningQuiz()
        setupQuestion(myQuizData!!, currentSubjectIndex, currentQuestionIndex)
        binding.previousQuestionButton.setOnClickListener{
            if (currentQuestionIndex > 0) {
                currentQuestionIndex -= 1
                setupQuestion(myQuizData, currentSubjectIndex, currentQuestionIndex)
            }
            else if (currentSubjectIndex > 0) {
                currentSubjectIndex -= 1
                currentQuestionIndex = myQuizData.quiz_data.get(currentSubjectIndex).ids.lastIndex
                setupQuestion(myQuizData, currentSubjectIndex, currentQuestionIndex)
            }
            else{

            }
        }
        binding.nextQuestionButton.setOnClickListener{
            if (currentQuestionIndex < myQuizData.quiz_data.get(currentSubjectIndex).ids.size - 1) {
                currentQuestionIndex += 1
                setupQuestion(myQuizData, currentSubjectIndex, currentQuestionIndex)
            }
            else if (currentSubjectIndex < myQuizData.quiz_data.size - 1) {
                currentSubjectIndex += 1
                currentQuestionIndex = 0
                setupQuestion(myQuizData, currentSubjectIndex, currentQuestionIndex)
            }
            else{
                val alertUtils = AlertUtils(requireContext())
                alertUtils.showAlert("Submit?", "Will you like to submit your quiz?", "YES"){
                    markAnswers()
                }
            }
        }

    }

    fun markAnswers(){
        Log.d("CORRECT", "MARK ANSWERS")
        var totalCorrect = 0
        var totalAnswered = 0
        var totalQuestions = 0

        val quizEndSubjects = mutableListOf<QuizEndSubject>()
        for(i in 0..myQuizData.quiz_data.size - 1){
            var subjectScore = 0
            var subjectQuestions = 0
            var subjectName = ""
            for(j in 0..myQuizData.quiz_data.get(i).ids.size - 1){
                subjectQuestions+=1
                totalQuestions += 1

                if (runningQuiz.answers[i][j] != 'O') {
                    totalAnswered += 1

                    if (runningQuiz.correctAnswers[i][j] == runningQuiz.answers[i][j]){
                        subjectScore += 1
                        totalCorrect += 1
                    }
                }
            }
            val quizEndSubject = QuizEndSubject(
                myQuizData.quiz_data.get(i).subjectId,
                myQuizData.quiz_data.get(i).subject,
                subjectScore,
                subjectQuestions
            )
            quizEndSubjects.add(quizEndSubject)
        }
        Log.d("MARKING", totalCorrect.toString())
        Log.d("MARKING", totalAnswered.toString())
        Log.d("MARKING", totalQuestions.toString())
        val quizEndData = QuizEndData(
            myQuizData.mock_id,
            myQuizData.quiz_data.size,
            totalCorrect,
            totalQuestions,
            quizEndSubjects
        )
        val bundle = Bundle()
        bundle.putSerializable("my_quiz_end_data", quizEndData)
        bundle.putSerializable("my_running_quiz", runningQuiz)
        bundle.putSerializable("my_quiz_data", myQuizData)
        Log.d("INSIDE", quizEndData.nSubjects.toString())
        Log.d("INSIDE", runningQuiz.correctAnswers.size.toString())
        Log.d("INSIDE", myQuizData.duration.toString())
        if (this.isAdded)
        findNavController().navigate(R.id.quiz_to_score, bundle)

        //Toast.makeText(requireContext(), "CORRECT - "+totalCorrect.toString(), Toast.LENGTH_LONG).show()
    }
    override fun onTimerFinished() {
        if (this.isAdded) {
        Log.d("TIMER FINISHED", "GO AND SUBMIT")
        val alertUtils = AlertUtils(requireActivity())
        alertUtils.showAlert("Time is up", "Sorry, your time is up, now you will be required to submit your mock for grading", "OK"){
            markAnswers()
        }
        binding.nextQuestionButton.visibility = View.GONE
        binding.previousQuestionButton.visibility = View.GONE
        binding.submitQuizButton.visibility = View.GONE;
        }

        // Callback logic when the timer finishes
        // You can perform actions here when the timer stops
    }

    private fun initializeRunningQuiz(): MutableList<MutableList<Char>> {
        val answers = mutableListOf<MutableList<Char>>()
        val correctAnswers = mutableListOf<MutableList<Char>>()

        for (i in 0..myQuizData.quiz_data.size - 1){
            val oneSubjectAnswers = mutableListOf<Char>()
            val oneSubjectCorrectAnswers = mutableListOf<Char>()
            for(j in 0..myQuizData.quiz_data.get(i).ids.size - 1){
                oneSubjectAnswers.add('O')
                oneSubjectCorrectAnswers.add('O')
            }
            answers.add(oneSubjectAnswers)
            correctAnswers.add(oneSubjectCorrectAnswers)
        }
        runningQuiz = QuizRunning(answers, correctAnswers, 0, 0)
        val timer = TimerUtils(binding.quizTimer, myQuizData.duration)
        timer.setCallback(this)
        timer.start()
        return answers;
    }

    private fun setupQuestion(quizData: ResponseQuizData, subjectIndex: Int, questionIndex: Int) {
        val subject = quizData.quiz_data.get(subjectIndex).subject
        //val questionUrl = "${resources.getString(R.string.root_url)}${GET_QUESTIONS_ENPOINT}/level/${quizData.quiz_data.get(0).level}/category/${quizData.quiz_data.get(0).subjectId}?n=1"
        if (quizData.quiz_data.size <= 0 || quizData.quiz_data.get(subjectIndex).ids.size <= 0) {
            val alertUtils = AlertUtils(requireContext())
            alertUtils.showAlert("No questions found", "There are no questions available in "+subject, "O.K"){
                //findNavController().navigate(R.id.quiz_to_home)
            }
            return
        }
        val questionUrl = "${resources.getString(R.string.root_url)}${GET_QUESTION_ENPOINT}/${quizData.quiz_data.get(subjectIndex).ids.get(questionIndex)}"
        val getQuestionService = UrlFetchService(questionUrl)
        val callback = object : Callback {
            override fun onResponse(call: Call, response: Response) {
                // Handle the response here
                val responseBody = response.body?.string()
                Log.d("GET QUESTION", responseBody.toString())
                val responseQuestion = Gson().fromJson(responseBody.toString(), Question::class.java)
                var myScope = CoroutineScope(Dispatchers.Main);
                myScope.launch { updateQuestionDataView(subjectIndex, subject, responseQuestion, questionIndex) }
            }

            override fun onFailure(call: Call, e: IOException) {
                Log.d("USERREG", e.message.toString())
                // Handle any network or request errors here
            }
        }
        getQuestionService.fetchUrl("GET","", callback)
    }

    fun updateQuestionDataView(
        subjectIndex: Int,
        subjectName: String,
        question: Question,
        questionNumber: Int
    ){
        if (!this.isAdded) {
            return
        }
        clearSelection()
        binding.subjectName.text = subjectName
        binding.questionNumber.text = "Question: "+(questionNumber + 1).toString()
        binding.questionText.text = question.question_text
        binding.optionA.text = question.option_a
        binding.optionB.text = question.option_b
        binding.optionC.text = question.option_c
        binding.optionD.text = question.option_d
        if (question.option_e != "") {
            binding.optionELayout.visibility = View.GONE
        }
        if (quizMode == "MOCK_MODE") {
            runningQuiz.correctAnswers[subjectIndex][questionNumber] = question.correct_options[0]
            Log.d("CORRECT", runningQuiz.answers.joinToString())
            when (runningQuiz.answers[subjectIndex][questionNumber]) {
                'A' -> binding.optionA.isChecked = true
                'B' -> binding.optionB.isChecked = true
                'C' -> binding.optionC.isChecked = true
                'D' -> binding.optionD.isChecked = true
                'E' -> binding.optionE.isChecked = true
//          'O' -> binding.optionsRadioGroup.clearCheck()
            }
        }
        else {
            Log.d("FREE MODE", "YES")
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
    private fun clearSelection(){
        binding.optionA.setBackgroundColor(Color.WHITE)
        binding.optionB.setBackgroundColor(Color.WHITE)
        binding.optionC.setBackgroundColor(Color.WHITE)
        binding.optionD.setBackgroundColor(Color.WHITE)
        binding.optionE.setBackgroundColor(Color.WHITE)

        binding.optionA.isChecked = false
        binding.optionB.isChecked = false
        binding.optionC.isChecked = false
        binding.optionD.isChecked = false
        binding.optionE.isChecked = false
    }
    fun getQuestion(){

            val url = "${resources.getString(R.string.root_url)}${GET_QUESTION_ENPOINT}"
            val getQuestionService = UrlFetchService(url)
            val callback = object : Callback {
                override fun onResponse(call: Call, response: Response) {
                    // Handle the response here
                    val responseBody = response.body?.string()
                    Log.d("USERREG", responseBody.toString())
                    val gson = Gson()
                    val response = gson.fromJson(responseBody.toString(), BackendResponse::class.java)
                    val token = response.access_token
                    if (token != ""){
                        val alertUtils = AlertUtils(requireContext()) // 'this' is the context of your activity or fragment
                        // Display an alert
                        val myScope = CoroutineScope(Dispatchers.Main)
                        myScope.launch {
                            PrefsManager.getInstance(requireContext()).saveJwt(token)
                            alertUtils.showAlert("Log in Successfful", "You have successfully logged in", "OK"){
                                findNavController().navigate(R.id.login_to_home)
                            }
                        }
                    }
                    Log.d("USERREG", token)
                }

                override fun onFailure(call: Call, e: IOException) {
                    Log.d("USERREG", e.message.toString())
                    // Handle any network or request errors here
                }
            }
        getQuestionService.fetchUrl("GET","", callback)
    }
    override fun onResume() {
        super.onResume()
        val storedQuizData = PrefsManager.getInstance(requireContext()).getQuizData()
        if (storedQuizData == null && quizMode == "MOCK_MODE"){
           /* val alertUtils = AlertUtils(requireContext())
            alertUtils.showAlert("Quiz completed", "Current quiz completed. Return to select another quiz", "YES"){
                findNavController().navigate(R.id.quiz_to_home)
            }*/
            findNavController().navigate(R.id.quiz_to_home)

        }
    }
}