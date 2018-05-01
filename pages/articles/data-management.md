---
type: article
title: 데이터 관리
date: Feb 9, 2013
summary: 기록 덕후의 데이터 저장 관리 방법
---

어렸을 때 부터 손으로 써서든 타이핑을 해서든, 무언가를 만드는 일을 계속 해오다 보니 나는 남들보다 내가 만든 또는 내가 얻은 데이터에 대해 애착을 갖는 편이다. 애착을 갖는 다는 것은 별다르게 특별한 것을 의미하는 것은 아니고, 언제나 내가 했던 기록을 열어볼 수 있는 정도로 정리해놓는 것을 의미한다. 쉽게 열어볼 수 있도록 폴더 구조를 잘 구축해 놓는 것도 내가 데이터에게 해주는 작업 중 하나이다.

주로 프로그래밍을 많이 했기 때문에, 대부분의 가지고 있는 데이터는 디지털로 되어있지만, 일부 데이터(예를 들면, 고등학교 때 푼 수능 문제의 풀이과정[^1]이라던가, 지인들에게 받은 편지들 등)는 아날로그로 되어있기도 하다.

최근에 데이터 관리하는 방법을 변경하려 조금씩 작업을 진행하고 있는데, 눈여겨볼 만한 변화라면 모든 문서의 LaTeX 소스코드화와 소스코드 저장소 호스팅을 적극적으로 이용하는 문서 저장이라고 할 수 있다.

LaTeX이 기존의 문서와 다른 점은 문서가 코드로 존재하기 때문에 텍스트 형식으로 존재한다는 점이다. 따라서 소스코드 관리 시스템으로 쉽게 관리할 수 있다는 장점이 있다. 협업도 당연히 쉬워지는 편이다. 출력해서 종이로 만드는 경우를 위해 탄생된 시스템이라 출력된 결과물도 이쁘게 뽑을 수 있다.[^2] 또 하나의 특징은 큰 틀에서 표현과 내용을 분리할 수 있다는 점이다. 다만, 완벽하지는 않다.

시간이 되는 대로, 대학교 때 썼던 레포트들을 LaTeX 형태로 변환하여 소스코드 저장소에 저장하고 있다. 코드는 Bitbucket 저장소에 공개되어 있으며, 다운로드 페이지에서 PDF로 변환된 문서도 받아볼 수 있다. 언제나 그렇듯이 레포트를 작성하는 시점에 내 의견과 지금의 내 의견은 다를 수도 있고 또 약간 과장하거나 사실인지 불분명한 내용이 들어있기도 하다. 그것도 나의 생각이었으니 숨기지 않고 공개해야겠다는 마음으로 변환 작업을 계속하고 있다.

이제 2개 수업에서 작성했던 문서를 변환했는데, 아직도 많은 문서가 남아있다. 틈틈이 또 꾸준히 바꿔서 졸업하기 전에 모든 문서를 LaTeX로 바꿀 수 있도록 해야겠다.

[^1]: 문제집과 공부할 때 사용했던 노트를 버리지 않고 가지고 있다.

[^2]: 저게 사실상의 장점의 전부고, 사실 단점도 만만찮게 많다. 수식을 깔끔하게 입력할 수 있다는 장점도 있으나, 일반적인 문서에서 수식을 자주 쓰지는 않기 때문에 아주 큰 메리트라고 보기는 어렵다. 문서 작성시간도 일반적인 워드프로세서에 비해 평균적으로 오래걸리는 편이며, 커스터마이징을 하려면 대단한 노력이 필요하다. 협업을 하려해도 협업에 참여하는 모든 사람이 LaTeX에 수준급의 실력을 갖추고 있어야한다.