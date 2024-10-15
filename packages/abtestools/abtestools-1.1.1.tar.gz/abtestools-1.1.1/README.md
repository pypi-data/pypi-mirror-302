
<a id="readme-top"></a>
<!--
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/pablominue/pyabtesting">
    <img src="images/abtestools.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">pyabtesting</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/pablominue/pyabtesting"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/pablominue/pyabtesting">View Demo</a>
    ·
    <a href="https://github.com/pablominue/pyabtesting/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/pablominue/pyabtesting/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This library provides tools for AB Testing, very useful when working with marketing data

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

To develop on this project, you will need to create a poetry environment with the needed dependencies
* install with Poetry
  ```sh
  poetry install
  ```

### Installation


1. 
   ```sh
   git clone https://github.com/pablominue/pyabtesting.git
   ```
   or
   ```sh
   pip install abtestools
   ```

3. Import main modules
   ```python
   from abtestools import audience, test
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage


```python
import datetime

import pandas as pd

from abtestools.audiences import Audience
from abtestools.campaign import Campaign
from abtestools.test import Metric

data = pd.read_csv("tests/cookie_cats.txt", delimiter=",")

audience = Audience(
    users=data["userid"], group_mapping=dict(zip(data["userid"], data["version"]))
)

campaign = Campaign(
    audience=audience,
    metrics=[
        Metric(name="retention_1", type="discrete"),
        Metric(name="retention_7", type="discrete"),
    ],
    date_range=[
        datetime.datetime.today() - datetime.timedelta(days=x) for x in range(10)
    ],
)


def extract_data(date, metric_column: str, convert_bool: bool = True) -> dict:
    # Logic for each date calculation should be added here
    if convert_bool:
        data[metric_column] = data[metric_column].astype(int)
    return dict(zip(data["userid"], data[metric_column]))


for res in campaign.backfill(
    metric=Metric(name="retention_1", type="discrete"),
    extract_data=extract_data,
    metric_column="retention_1",
):
    print(res)

```

 
<!-- ROADMAP -->
<!--
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/pablominue/pyabtesting/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
<!--
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/pablominue/pyabtesting/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pablominue/pyabtesting" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
<!--
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
<!--
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!--
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]:https://img.shields.io/github/contributors/pablominue/pyabtesting
[contributors-url]: https://github.com/pablominue/pyabtesting/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/pablominue/pyabtesting.svg?style=for-the-badge
[forks-url]: https://github.com/pablominue/pyabtesting/network/members
[stars-shield]: https://img.shields.io/github/stars/pablominue/pyabtesting.svg?style=for-the-badge
[stars-url]: https://github.com/pablominue/pyabtesting/stargazers
[issues-shield]: https://img.shields.io/github/issues/pablominue/pyabtesting.svg?style=for-the-badge
[issues-url]: https://github.com/pablominue/pyabtesting/issues
[license-shield]: https://img.shields.io/github/license/pablominue/pyabtesting.svg?style=for-the-badge
[license-url]: https://github.com/pablominue/pyabtesting/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/pablo-minue/
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[python-url]: https://python.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 