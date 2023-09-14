package com.haneef.medquiz

import android.content.Context
import android.graphics.Color
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
import androidx.recyclerview.widget.RecyclerView
import com.haneef.medquiz.multilevelview.MultiLevelAdapter
import com.haneef.medquiz.multilevelview.MultiLevelRecyclerView
import java.util.Locale


class MyAdapter internal constructor(

    mContext: Context,
    mListItems: List<Item>,
    mMultiLevelRecyclerView: MultiLevelRecyclerView
) :
    MultiLevelAdapter(mListItems) {
    private var mViewHolder: Holder? = null
    private val mContext: Context
    private var mListItems: List<Item> = ArrayList()
    private var mItem: Item? = null
    private val mMultiLevelRecyclerView: MultiLevelRecyclerView

    init {
        this.mListItems = mListItems
        this.mContext = mContext
        this.mMultiLevelRecyclerView = mMultiLevelRecyclerView
    }

    private fun setExpandButton(expandButton: ImageView, isExpanded: Boolean) {
        // set the icon based on the current state
        expandButton.setImageResource(if (isExpanded) R.drawable.baseline_keyboard_double_arrow_up_24 else R.drawable.baseline_keyboard_double_arrow_down_24)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        return Holder(
            LayoutInflater.from(parent.context).inflate(R.layout.item_layout, parent, false)
        )
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        mViewHolder = holder as Holder
        mItem = mListItems[position]
        when (getItemViewType(position)) {
            0 -> holder.itemView.setBackgroundColor(Color.parseColor("#efefef"))
            1 -> holder.itemView.setBackgroundColor(Color.parseColor("#dedede"))
            2 -> holder.itemView.setBackgroundColor(Color.parseColor("#cdcdcd"))
            else -> holder.itemView.setBackgroundColor(Color.parseColor("#ffffff"))
        }

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

        val density = mContext.resources.displayMetrics.density
        (mViewHolder!!.mTextBox.layoutParams as MarginLayoutParams).leftMargin =
            (getItemViewType(position) * 20 * density + 0.5f).toInt()
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
            mExpandButton.setOnClickListener {
                mMultiLevelRecyclerView.toggleItemsGroup(adapterPosition)
                mExpandIcon.animate()
                    .rotation((if (mListItems[adapterPosition].isExpanded) -180 else 0).toFloat())
                    .start()
                Toast.makeText(
                    mContext, String.format(
                        Locale.ENGLISH, "Item at position %d is expanded: %s",
                        adapterPosition, mItem!!.isExpanded
                    ), Toast.LENGTH_SHORT
                ).show()
            }
        }
    }
}
