package com.haneef.medquiz.ui.home

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.google.gson.Gson
import com.haneef.medquiz.Category
import com.haneef.medquiz.Item
import com.haneef.medquiz.MyAdapter
import com.haneef.medquiz.R
import com.haneef.medquiz.Subcategory
import com.haneef.medquiz.Subject
import com.haneef.medquiz.Unit
import com.haneef.medquiz.databinding.FragmentHomeBinding
import com.haneef.medquiz.multilevelview.models.RecyclerViewItem
import com.haneef.medquiz.network.NetworkHandler
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val homeViewModel =
            ViewModelProvider(this).get(HomeViewModel::class.java)

        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root

        /*val textView: TextView = binding.textHome
        homeViewModel.text.observe(viewLifecycleOwner) {
            textView.text = it
        }*/

        readCategoriesFromBackend()

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

    private fun readCategoriesFromBackend(): List<Category> {
        val myScope = CoroutineScope(Dispatchers.IO)
        var categoriesJson = ""
        var categoriesList = listOf<Category>()
        Log.d("CATS", "HERE")
        myScope.launch {
            val networkHandler = NetworkHandler(requireActivity(), null, false)
            categoriesJson = networkHandler.fetchWebPageContent("${resources.getString(R.string.root_url)}/quiz/get_all_categories")
            Log.d("CATS2", categoriesJson)
            if (categoriesJson != ""){
                categoriesList = Gson().fromJson(categoriesJson, Array<Category>::class.java).toList()
                withContext(Dispatchers.Main){
                    Log.d("CATS3", categoriesList.size.toString())
                    val itemList = recursivePopulateCategories(categoriesList, 0, categoriesList.size) as List<Item>
                    val myAdapter = MyAdapter(requireContext(), itemList, binding.multilevelRecycler)
                    binding.multilevelRecycler.adapter = myAdapter
                }
            }
        }

        return categoriesList
    }

    private fun recursivePopulateCategories(itemsList: List<Any>, levelNumber: Int, depth: Int): List<*>? {
        val displayList: MutableList<RecyclerViewItem> = ArrayList()


        for (i in 0 until depth) {


            val objectToItem = when (levelNumber) {
                0 -> {
                    val category = itemsList[i] as Category
                    val item = Item(levelNumber).apply {
                        text = String.format(Locale.ENGLISH, category.name, i)
                        secondText = String.format(Locale.ENGLISH, category.subcategories.size.toString() + " subcategories", i)
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
                        text = String.format(Locale.ENGLISH, subcategory.name, i)
                        secondText = String.format(Locale.ENGLISH, subcategory.subjects.size.toString() + " subjects", i)
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
                        text = String.format(Locale.ENGLISH, subject.name, i)
                        secondText = String.format(Locale.ENGLISH, subject.units.size.toString() + " units", i)
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
                        text = String.format(Locale.ENGLISH, unit.name, i)
                        if (unit.tags != null) secondText = String.format(Locale.ENGLISH, unit.tags.size.toString() + " tags", i)
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
                        text = String.format(Locale.ENGLISH, unit, i)
                        secondText = String.format(Locale.ENGLISH, " questions", i)
                    }
                }
            }


            displayList.add(objectToItem)
        }
        return displayList
    }

}