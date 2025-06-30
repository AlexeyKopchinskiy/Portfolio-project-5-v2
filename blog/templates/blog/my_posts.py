{% extends 'base.html' %}
{% block content %}
  <div class="container mt-4">
    <h2>My Posts</h2>
    <ul class="list-group">
      {% for post in posts %}
        <li class="list-group-item">
          <a href="#">{{ post.title }}</a> — {{ post.created|date:"M d, Y" }}
        </li>
      {% empty %}
        <li class="list-group-item">You haven't published anything yet.</li>
      {% endfor %}
    </ul>
  </div>
{% endblock %}