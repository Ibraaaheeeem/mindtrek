package com.haneef.medquiz

import com.haneef.medquiz.multilevelview.models.RecyclerViewItem


class Item (level: Int) : RecyclerViewItem(level) {
    var id = 0
    var text = ""
    var secondText = ""
}
