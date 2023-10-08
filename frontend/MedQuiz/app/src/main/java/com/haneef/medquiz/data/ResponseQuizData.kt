package com.haneef.medquiz.data

import java.io.Serializable

data class ResponseQuizData (var quiz_data: MutableList<QuizData>, val mock_id: Int, val duration: Long, val msg: String): Serializable
data class QuizData (val ids: List<Int>, val level: Int, val subject: String, val subjectId: Int): Serializable
data class QuizRunning (var answers: MutableList<MutableList<Char>>, val correctAnswers: MutableList<MutableList<Char>>, var lastSubjectIndex: Int, var lastQuestionIndex: Int): Serializable
/*
data class QuizQuestionIds(val subject: String, val ids: List<Int>)*/
