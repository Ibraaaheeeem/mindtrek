package com.haneef.medmcq.data

class MockSubject(val name: String, var totalQuestions: Int, var score: Int){

    fun setQuestionCount(count: Int) {
        totalQuestions = count
    }
}