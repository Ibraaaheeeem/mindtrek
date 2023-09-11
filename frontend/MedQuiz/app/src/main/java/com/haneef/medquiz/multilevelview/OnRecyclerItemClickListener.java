package com.haneef.medquiz.multilevelview;

import android.view.View;

import com.haneef.medquiz.multilevelview.models.RecyclerViewItem;

public interface OnRecyclerItemClickListener {
    void onItemClick(View view, RecyclerViewItem item, int position);
}