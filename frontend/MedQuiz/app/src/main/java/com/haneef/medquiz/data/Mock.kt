package com.haneef.medmcq.data

class Mock(val userName: String,  val score: Int){
    val subjects: MutableList<MockSubject>? = null
    fun addSubject(subjectName: String) {
        val newSubject = MockSubject(subjectName, 0, 0)
        subjects?.add(newSubject)
    }

    // Function to set the score for a subject
    fun setSubjectScore(subjectName: String, score: Int) {
        val subject = subjects?.find { it.name == subjectName }
        subject?.score = score
    }

    // Function to get the total score for the mock exam
    fun getTotalScore(): Int {
        return subjects?.sumBy { it.score } ?: 0
    }

    // Function to get the average score for the mock exam
    fun getAverageScore(): Double {
        return if (subjects?.isNotEmpty() == true) {
            getTotalScore().toDouble() / subjects.size.toDouble()
        } else {
            0.0
        }
    }

    // Function to display the exam results
    fun displayResults(studentName: String) {
        println("Mock Exam Results for $studentName:")
        if (subjects != null) {
            for (subject in subjects) {
                println("${subject.name}: ${subject.score}")
            }
        }
        println("Total Score: ${getTotalScore()}")
        println("Average Score: ${getAverageScore()}")
    }
}