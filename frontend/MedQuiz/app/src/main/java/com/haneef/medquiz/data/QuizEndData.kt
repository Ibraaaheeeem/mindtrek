package com.haneef.medquiz.data

import java.io.Serializable

class QuizEndData(val id: Int, val nSubjects: Int, val totalScore: Int, val totalPossibleScore: Int, val subjects: List<QuizEndSubject>): Serializable
class QuizEndSubject(val id: Int, val name: String, val score: Int, val totalSubjectScore: Int) : Serializable