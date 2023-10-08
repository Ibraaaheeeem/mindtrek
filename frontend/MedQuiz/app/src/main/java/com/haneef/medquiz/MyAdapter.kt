package com.haneef.medquiz

import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.ViewGroup.MarginLayoutParams
import android.widget.EditText
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.RecyclerView
import com.haneef.medquiz.multilevelview.MultiLevelAdapter
import com.haneef.medquiz.multilevelview.MultiLevelRecyclerView
import com.haneef.medquiz.utils.PrefsManager
import java.util.Locale

class MyAdapter internal constructor(

    mContext: Context,
    var mTestStyle: Int,
    mListItems: List<Item>,
    val mockSubjectsLayout: LinearLayout,
    mMultiLevelRecyclerView: MultiLevelRecyclerView,
    private val navigationListener: FragmentNavigationListener
) :
    MultiLevelAdapter(mListItems) {
    private var mViewHolder: Holder? = null
    private val mContext: Context
    private var mListItems: List<Item> = ArrayList()
    private var mItem: Item? = null
    private val mMultiLevelRecyclerView: MultiLevelRecyclerView
    private var mock = Mock("user", 0)
    private val MOCK_STYLE_TEST = 9
    private val FREE_STYLE_TEST = 10

    fun getMock(): Mock{
        return mock
    }

    init {
        this.mListItems = mListItems
        this.mContext = mContext
        this.mMultiLevelRecyclerView = mMultiLevelRecyclerView
    }

    private fun setExpandButton(expandButton: ImageView, isExpanded: Boolean) {
        // set the icon based on the current state

        Log.d("EXPANDED", ""+isExpanded)
        //expandButton.setImageResource(if (isExpanded) R.drawable.baseline_keyboard_double_arrow_up_24 else R.drawable.baseline_keyboard_double_arrow_down_24)
        expandButton.setImageResource(R.drawable.baseline_keyboard_double_arrow_down_24)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        return Holder(
            LayoutInflater.from(parent.context).inflate(R.layout.item_layout, parent, false)
        )
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        mViewHolder = holder as Holder
        mItem = mListItems[position]
        val plusButton = holder.itemView.findViewById<ImageView>(R.id.addToMock)
        val playButton = holder.itemView.findViewById<ImageView>(R.id.startFreeStyle)
        val categoryLevel = getItemViewType(position)
        val layoutParams = LinearLayout.LayoutParams(holder.itemView.findViewById<TextView>(R.id.levelsign).layoutParams)
        when (categoryLevel) {

            0 -> {
                holder.itemView.setBackgroundColor(Color.parseColor("#efefff"))
                layoutParams.setMargins(0, 0, 0, 0)
                holder.itemView.findViewById<TextView>(R.id.levelsign).setTextColor(Color.BLUE)
                holder.itemView.findViewById<TextView>(R.id.levelsign).layoutParams = layoutParams
            }
            1 -> {
                holder.itemView.setBackgroundColor(Color.parseColor("#dedeee"))
                //layoutParams.setMargins(50, 0, 0, 0)
                holder.itemView.findViewById<TextView>(R.id.levelsign).text = ">>"
                holder.itemView.findViewById<TextView>(R.id.levelsign).setTextColor(Color.RED)
                holder.itemView.findViewById<TextView>(R.id.title).setTextColor(Color.RED)
                holder.itemView.findViewById<TextView>(R.id.levelsign).layoutParams = layoutParams
            }
            2 -> {
                holder.itemView.setBackgroundColor(Color.parseColor("#cdcddd"))
                //layoutParams.setMargins(100, 0, 0, 0)
                holder.itemView.findViewById<TextView>(R.id.levelsign).text = ">>>"
                holder.itemView.findViewById<TextView>(R.id.levelsign).setTextColor(Color.parseColor("#558855"))
                holder.itemView.findViewById<TextView>(R.id.title).setTextColor(Color.parseColor("#558855"))
                holder.itemView.findViewById<TextView>(R.id.levelsign).layoutParams = layoutParams
            }
            3 -> {
                holder.itemView.setBackgroundColor(Color.parseColor("#ffffcc"))
                holder.itemView.findViewById<TextView>(R.id.levelsign).text = ">>>>"
                holder.itemView.findViewById<TextView>(R.id.levelsign).setTextColor(Color.MAGENTA)
                holder.itemView.findViewById<TextView>(R.id.title).setTextColor(Color.MAGENTA)
                //layoutParams.setMargins(150, 0, 0, 0)
                holder.itemView.findViewById<TextView>(R.id.levelsign).layoutParams = layoutParams
            }
            else -> {
                holder.itemView.setBackgroundColor(Color.parseColor("#ffffff"))
                //layoutParams.setMargins(200, 0, 0, 0)
                holder.itemView.findViewById<TextView>(R.id.levelsign).layoutParams = layoutParams
            }
        }
        when (mTestStyle){
            MOCK_STYLE_TEST -> {
                plusButton.visibility = View.VISIBLE
                playButton.visibility = View.GONE
            }
            else -> {
                plusButton.visibility = View.GONE
                playButton.visibility = View.VISIBLE
            }
        }
        playButton.tag = mItem!!
        playButton.setOnClickListener{
            val sbj = it.tag as Item
            val bundle = Bundle()
            bundle.putInt("subject_id", sbj.id)
            bundle.putString("subject_name", sbj.text)
            bundle.putInt("subject_level", categoryLevel+1)
            PrefsManager.getInstance(mContext).saveQuizMode("FREE_MODE")
            navigationListener.navigateToFragment(R.id.home_to_quiz, bundle)
        }

        plusButton.setOnClickListener{
            Toast.makeText(
                mContext, String.format(
                    Locale.ENGLISH, "Item at position %s was clicked!",
                    it.tag as String
                ), Toast.LENGTH_SHORT
            ).show()
            Log.d("MOCK", "NO LONGER NULL")
            mock.addSubject(it.tag as String, categoryLevel+1)
            Log.d("MOCK", it.tag.toString()+"-"+mock.subjects?.size.toString())
            updateMockSubjects(mock)
            Log.d("MOCK", "mock")
        }
        plusButton.tag = mItem!!.text
        mViewHolder!!.mTitle.text = mItem!!.text
        mViewHolder!!.mSubtitle.text = mItem!!.secondText
        if (mItem!!.hasChildren() && mItem!!.children.size > 0) {
            setExpandButton(mViewHolder!!.mExpandIcon, mItem!!.isExpanded)
            mViewHolder!!.mExpandButton.visibility = View.VISIBLE
        } else {
            mViewHolder!!.mExpandButton.visibility = View.GONE
        }
        Log.e(
            "MuditLog",
            mItem!!.level.toString() + " " + mItem!!.position + " " + mItem!!.isExpanded + ""
        )
        // indent child items
        // Note: the parent item should start at zero to have no indentation
        // e.g. in populateFakeData(); the very first Item shold be instantiate like this: Item item = new Item(0);
        val density = mContext.resources.displayMetrics.density
        (mViewHolder!!.mTextBox.layoutParams as MarginLayoutParams).leftMargin =
            (getItemViewType(position) * 20 * density + 0.5f).toInt()
    }

    fun setTestStyle(testStyle: Int) {
        mTestStyle = testStyle
    }

    fun updateMockSubjects(mock: Mock){
        Log.d("MOCK", "HERE")
        Log.d("MOCK", mock.subjects?.size.toString())
        mockSubjectsLayout.removeAllViews()
        mock.subjects?.forEachIndexed {index, it ->
            val view = LayoutInflater.from(mContext).inflate(R.layout.item_mock_subject, null, false)
            view.tag = it
            view.findViewById<TextView>(R.id.subjectTextView).text = (index + 1).toString() +". "+ it.name + " (${it.num_questions})"

            view.findViewById<TextView>(R.id.indexTextView).text = (index + 1).toString()
            val mockSubjectQuestionCount = view.findViewById<TextView>(R.id.editTextNumber)
            mockSubjectQuestionCount.text = it.num_questions.toString()
            val removeMockImageView = view.findViewById<ImageView>(R.id.removeMockImageView)
            val updateQuestionNumber = view.findViewById<ImageView>(R.id.updateQuestionNumber)
            updateQuestionNumber.setOnClickListener{
                val mockSubject = (it.parent as View).tag as MockSubject
                val countEditText = (it.parent as View).findViewById<EditText>(R.id.editTextNumber)
                if (countEditText.text.toString() == "") return@setOnClickListener
                mockSubject.setQuestionCount(countEditText.text.toString().toInt())
                updateMockSubjects(mock)
            }
            removeMockImageView.setOnClickListener{
                val mockSubject = (it.parent as View).tag as MockSubject
                mock.removeSubject(mockSubject)
                updateMockSubjects(mock)
            }
            /*mockSubjectQuestionCount.setOnFocusChangeListener { view, hasFocus ->
                val mockSubject = (view.parent as View).tag as MockSubject
                val countEditText = view as EditText
                if (countEditText.text.toString() == "") return@setOnFocusChangeListener
                mockSubject.setQuestionCount(countEditText.text.toString().toInt())
            }*/
            mockSubjectsLayout.addView(view)
        }

    }
    private inner class Holder internal constructor(itemView: View) :
        RecyclerView.ViewHolder(itemView) {
        var mTitle: TextView
        var mSubtitle: TextView
        var mExpandIcon: ImageView
        var mTextBox: LinearLayout
        var mExpandButton: LinearLayout
        var mPlusButton: ImageView

        init {
            mTitle = itemView.findViewById<View>(R.id.title) as TextView
            mSubtitle = itemView.findViewById<View>(R.id.subtitle) as TextView
            mExpandIcon = itemView.findViewById<View>(R.id.image_view) as ImageView
            mTextBox = itemView.findViewById<View>(R.id.text_box) as LinearLayout
            mExpandButton = itemView.findViewById<View>(R.id.expand_field) as LinearLayout
            mPlusButton = itemView.findViewById<View>(R.id.addToMock) as ImageView


            // The following code snippets are only necessary if you set multiLevelRecyclerView.removeItemClickListeners(); in MainActivity.java
            // this enables more than one click event on an item (e.g. Click Event on the item itself and click event on the expand button)
            itemView.setOnClickListener { //set click event on item here

            }

            //set click listener on LinearLayout because the click area is bigger than the ImageView
            itemView.findViewById<LinearLayout>(R.id.text_box).setOnClickListener { // set click event on expand button here
                mMultiLevelRecyclerView.toggleItemsGroup(adapterPosition)
                // rotate the icon based on the current state
                // but only here because otherwise we'd see the animation on expanded items too while scrolling
                mExpandIcon.animate()
                    .rotation((if (mListItems[adapterPosition].isExpanded) -180 else 0).toFloat())
                    .start()
                /*Toast.makeText(
                    mContext, String.format(
                        Locale.ENGLISH, "Item at position %d is expanded: %s",
                        adapterPosition, mItem!!.isExpanded
                    ), Toast.LENGTH_SHORT
                ).show()*/
            }
        }
    }
    interface FragmentNavigationListener {
        fun navigateToFragment(fragmentId: Int, bundle: Bundle)
    }

}
