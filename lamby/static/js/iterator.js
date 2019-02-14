function NodeIterator(baseId, start = 0) {
  this.baseId = baseId;
  this.index = start;
}

NodeIterator.prototype.hasNext = function() {
  return document.getElementById(`${this.baseId}-${this.index + 1}`) !== null;
};

NodeIterator.prototype.next = function() {
  return document.getElementById(`${this.baseId}-${++this.index}`);
};

NodeIterator.prototype.applyToAll = function(cb) {
  while (this.hasNext()) {
    const node = this.next();
    cb(node, this.index);
  }
};
