package com.haneef.medquiz.ui.quiz

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.haneef.medquiz.R
import com.haneef.medquiz.data.QuizEndData
import com.haneef.medquiz.databinding.FragmentScoresBinding
import com.haneef.medquiz.utils.PrefsManager

class ScoresFragment: Fragment() {
    private var _binding: FragmentScoresBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        Log.d("INSIDE", "SCOREFRAGMENT")
        _binding = FragmentScoresBinding.inflate(inflater, container, false)
        val bundle = arguments
        Log.d("MARKING2",bundle.toString())
        if (bundle != null) {
            val quizEndData = bundle.getSerializable("my_quiz_end_data") as QuizEndData?
            Log.d("MARKING2",quizEndData?.totalScore.toString())
            //val runningQuiz = bundle.getSerializable("my_running_quiz") as QuizRunning?
            if (quizEndData != null) {
                // Now you have the quizEndData object, use it as needed
            }
            binding.textViewScore.text = "Your Score: "+quizEndData?.totalScore+" / "+quizEndData?.totalPossibleScore
            for(i in 0..quizEndData?.nSubjects!! - 1){

                val view = LayoutInflater.from(requireContext()).inflate(R.layout.item_score, null, false)
                view.findViewById<TextView>(R.id.subjectName).text = quizEndData.subjects[i].name
                view.findViewById<TextView>(R.id.subjectScore).text = "Score: "+quizEndData.subjects[i].score+" / "+ quizEndData.subjects[i].totalSubjectScore
                binding.subjectScoresLayout.addView(view)
            }
        }
        else{
            Log.d("MARKING2","BUNDLE is null")
        }
        binding.buttonExit.setOnClickListener{
            PrefsManager.getInstance(requireContext()).clearQuizData()
            findNavController().navigate(R.id.score_to_home)
        }
        binding.buttonViewCorrection.setOnClickListener{
            findNavController().navigate(R.id.view_corrections, bundle)
        }
        binding.buttonTryAgain.setOnClickListener{
            findNavController().navigate(R.id.nav_quiz, bundle)
        }
        return binding.root
    }

    override fun onDestroy() {
        super.onDestroy()
        PrefsManager.getInstance(requireContext()).clearQuizData()
    }
}