### Hi there! 👋

- 🐍 Python software developer
- 💻 Co-Founder of PyBites
- 📚 Love books/reading

<table><tr><td valign="top" width="50%">

### Latest Bluesky posts

<ul>
{% for post in posts %}
  <li>
    {{ post.title }} ({{ post.date }}) - <a href="{{ post.url }}" target="_blank">link</a>
  </li>
{% endfor %}
</ul>

> <a href="https://bsky.app/profile/bbelderbos.bsky.social" target="_blank">Follow me &raquo;</a>


</td><td valign="top" width="50%">

### Latest Python tips

<ul>
{% for tip in tips %}
  <li>
    {{ tip.title }} ({{ tip.date }}) - <a href="{{ tip.url }}" target="_blank">link</a>
  </li>
{% endfor %}
</ul>

> <a href="https://github.com/bbelderbos/bobcodesit" target="_blank">More Python tips &raquo;</a>

</td>
</tr></table>

<a href="https://github.com/bbelderbos/bbelderbos/actions" target="_blank"><img src="https://github.com/bbelderbos/bbelderbos/workflows/Daily%20Update/badge.svg" align="right" alt="Build README"></a>Roll your own: <a href="https://pybit.es/articles/how-to-create-a-self-updating-github-readme/" target="_blank">How to create a self updating GitHub Readme</a>.