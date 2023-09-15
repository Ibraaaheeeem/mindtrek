package com.haneef.medquiz

data class Category(val id: Int, val name: String, val subcategories: List<Subcategory>)