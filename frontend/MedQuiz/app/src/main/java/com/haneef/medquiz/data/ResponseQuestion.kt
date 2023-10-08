package com.haneef.medquiz.data

data class ResponseQuestions(val count: Int, val questions: List<Question>)
data class Questions(val questions: List<Question>)
data class Question(val question_text: String, val option_a: String, val option_b: String, val option_c: String, val option_d: String, val option_e: String, val correct_options: List<Char>, val explanation: String)