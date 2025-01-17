아래 글은 논문 "A Neural Algorithm of Artistic Style" - CVPR의 [Image Style Transfer Using Convolutional Neural Networks](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf) -을 읽고 작성하였다. 논문을 번역하고 또, 해석하는데 필요한 추가적인 지식도 함께 정리하였다. 

## Abstract

이미지가 담은 내용을 다른 이미지의 화풍으로 표현하는 것은 어렵다. 그 이유는 이미지가 담고 있는 내용과 그 이미지의 스타일을 분리하는 것이 어렵기 때문이다. 우리는 물체 인식에 최적화된 CNN 모델을 통해 고수준의 이미지 정보를 추출했다. 이미지의 내용과 이미지 본연의 스타일을 분리/합성하는 Neural algorithm of Artistic Style 모델을 소개한다. 이 알고리즘은 어떠한 이미지의 내용을 유명한 작품들의 모습을 결합한 높은 퀄리티의 새로운 이미지를 생성한다. 우리는 CNN으로 학습된 이미지 표현에 대해 새로운 인사이트와 고수준 이미지 합성과 조작에 대한 잠재력을 소개한다.

> High perceptual quality image?  
> 사람의 시각에서 선명하고 품질이 좋은 이미지로, 색상이나 디테일 등 시각적 요소가 조화를 이루어 명확하고 자연스럽게 보이는 이미지를 말한다.

## 1. Introduction

이미지의 화풍을 다른 이미지로 옮기는 것은 이미지 텍스처(texture)를 옮기는 문제로 해석할 수 있다. 텍스처 전달의 목표는 원본 이미지의 내용을 보존하면서 텍스처를 합성하는 것이다. 픽셀을 리샘플링하여 텍스처를 합성하는 알고리즘은 이미 존재한다. 기존의 텍스처 전달 알고리즘은 대부분 타켓 이미지의 구조를 보존하는 다양한 방법을 사용하면서, 텍스처 합성에 non-parametric 방법을 사용한다.

> Non parameteric method?  
> 데이터에 대한 특정 분포를 가정하지 않는 방ㅂ버으로 높은 유연성을 가진다. KNN(K-Nearest Neighbors), SVM(Support Vector Machine) 등이 해당된다.

예를 들어, Efros와 Freeman은 텍스처 합성 절차를 제한하기 위해 타겟 이미지의 특징(이미지 pixel의 밝은 정도-intensity-와 같은)을 포함한 correspondence map을 사용했다. 

> Correspondence Map?  
> 컴퓨터 비전에서 이미지나 3D 데이터 간의 픽셀, 특징, 3D 포인터 대응을 표현한 지도를 말한다. 이를 통해 두 데이터 간의 변화, 비교 등이 가능하다.

Hertzman 등은 이미지 유추를 통해 이미 스타일이 적용된 이미지로 텍스처를 전달한다. Ashikhmin은 타겟 이미지의 대략적인 특징을 유지한채 고주파 텍스처 정보를 전달하는 것에 중점을 두었다. Lee 등은 엣지의 방향 정보를 통해 텍스처 전달 알고리즘을 향상시켰다. 

비록 이 알고리즘들이 뛰어난 결과를 냈지만, 모두 텍스처 전송에 타켓 이미지의 저수준 특징만을 사용하는 공통된 문제를 보였다. 이상적인 화풍 전달 알고리즘은 타겟 이미지로부터 의미있는 내용을 추출해야 하며, 이 내용을 원본 이미지의 스타일로 렌더링 할 수 있어야 한다. 따라서 기초적인 전제조건은 주어진 이미지의 내용과 스타일의 변경을 독립적으로 모델링하는 이미지 표현 방식을 찾아야 한다. 

이처럼 분해된 표현 방식은 다양한 조명에서의 얼굴이나 글자의 다른 폰트, 손으로 쓴 숫자, 주택 번호와 같은 일상 이미지들에 대해서만 다루어져왔다. 

이미지에서 내용을 분리하는 것은 매우 어려운 문제이다. 하지만 최근 deep CNN의 발전으로 고수준의 의미있는 정보를 추출하도록 학습 가능하게 되었다. CNN이 라벨링된 데이터가 충분히 제공된다면, 객체 인식, 텍스처 인식, 화풍 분석과 같은 컴퓨터 비전 영역에서 데이터 셋으로부터 고수준의 이미지 내용을 뽑을 수 있도록 일반화할 수 있음이 이미 증명되었다. 

## 2. Deep image representation

아래의 결과들은 인식된 물체의 위치를 지정할 수 있도록 학습된 VGG 네트워크를 사용하여 생성되었다. 우리는 19 레이어를 가진 VGG 네트워크 중 16개의 convolutional, 5개의 pooling 레이어를 normalize하여 제공된 feature space를 사용하였다. 

> featrue space?  
> 각 레이어의 입력으로, 하나의 레이어는 들어온 feature space를 변환(학습)하여 더 유용한 새로운 feature space를 생성한다.

우리는 이미지의 각 convolutional filter의 출력 평균값이 1이 되도록 가중치를 scaling하여 네트워크를 normalize 하였다. 이러한 re-scaling은 ReLu를 사용하기에 VGG 네트워크 output에 영향을 주지 않는다. fully connected 레이어는 사용하지 않았다. 이 모델은 open되어 있고, caffe 프레임워크에서 구할 수 있다. 이미지의 합성의 경우, maximum pooling 연산을 average pooling으로 바꾼 것이 더 효과가 있었다. 

### 2-1. Content representation

보통 네트워크는 레이어의 위치에 따라 점차 더 복잡해지는 비선형 필터 함수들로 정의된다. 따라서 입력 이미지 $\vec{x}$은 각 CNN의 레이어에서 주어진 필터에 따라 encoding된다.

<img src="docs/content_representation.png" width="600"/>

$N_l$개의 서로 다른 필터를 가진 레이어는 $N_l$개의 사이즈가 $M_l\;(M_l=height \times width)$인 feature map을 가진다. 
따라서 레이어 $l$에 대한 결과는 matrix $F^l\;(F^l \in R^{N_l \times M_l})$로 표현된다. $F_{ij}^l$은 레이어 $l$의 $j$위치, $i$번째 필터이다.

각 레이어에서 출력된 이미지 정보를 시각화하기 위해서 white noise image를 gradient descent를 통해 원본 이미지와 레이어의 출력이 유사하도록 학습시킨다. (=레이어의 feature map이 원본 이미지의 특징을 추출하도록 학습 시킨다.) 

$\vec{p}$를 원본 이미지, $\vec{x}$를 생성된 이미지라 하고, $P^l$, $F^l$을 레이어 $l$에서의 featrue map이라고 하자. 우리는 이 두 feature 표현 사이의 차이를 손실로 정의할 수 있다.

$$
L_{content}(\vec{p}, \vec{x}, l) = frac{1}{2} sum_{i,j} (F_{ij}^l - P_{ij}^l)^2
$$

레이어 $l$에서의 activation 대한 loss의 미분은 이미지 $\vec{x}$를 표준 에러 back-propagation을 사용해 편미분한 값과 동일하다.

$$
\begin{align*}
\frac{\partial L_{content}}{\partial F_{ij}^l} = 
\begin{cases} 
(F^l - P^l)_{ij} &\text{if}\;F_{ij}^l > 0 \\
0 &\text{if}\;F_{ij}^l < 0 
\end{cases}
\end{align*}
$$

따라서 초기 랜덤 이미지 $\vec{x}$를 원본 이미지 $\vec{p}$와 동일하게 생성될 때까지 특정 레이어에서 변경할 수 있다.
CNN이 물체 인식으로 학습될 때, CNN은 계층을 따라 물체 정보를 더 명확하게 표현할 수 있도록 학습된다. 
결국, 네트워크를 따라 입력 이미지는 이미지의 내용에 대해서 민감하게 표현하도록 변하지만, 이미지의 세부 사항(모양의 왜곡, 조명, 회전 등)에 대해서는 영향을 덜 받는다. 

// 이미지

> 각 이미지들은 VGG 네트워크의 `conv1_2` (a),
`conv2_2` (b), `conv3_2` (c), `conv4_2` (d) 그리고 `conv5_2` (e) 레이어들로부터 얻었다.

따라서 높은 레이어일수록(d,e) 입력 이미지의 고수준의 내용을 담고 있지만 픽셀들마다의 정확한 value값을 변화하진 않는다. 반대로, 낮은 단계에서의 이미지 생성(a-c단계)은 원본 이미지의 정확한 pixel value값을 출력한다. 따라서 높은 레이어를 content representation이라고 정의한다.

// 이미지

### 2-2. Style representation

입력 이미지의 스타일 표현을 얻기 위해서 질감 정보를 얻는 feature space를 정의했다. 이러한 feature space는 네트워크의 어떠한 레이어의 필터에서든 만들어질 수 있다. 이는 피처맵의 공간적 부분에 대한 평균을 통해 다른 필터 결과 (특징들)사이의 상관관계를 포함한다. 
이 피처 상관관계는 gram matrix $G^l \in R^{N_l \times N_l} $에 의해서 제공되며, $G_{ij}^l$는 레이어 l의 피처맵 i와j와의 inner product로 계산된다.

$$
G_{ij}^l = \sum_k F_{ik}^l F_{jk}^l
$$

여러 레이어의 피처 상관관계를 포함시킴으로써, 우리는 입력 이미지에 대해 안정적이고, 여러 스케일로의 표현을 얻는다.(구성이 아닌 질감에 대한 정보를 담고 있다.) 

> global arrangement?  
> 이미지 전체에서 물체들이 어떻게 배열되고 배치되어 있는지에 대한 정보를 말한다. 예를 들어, 얼굴 사진에서 사람의 눈, 코, 입의 위치 등을 의미한다.  
> 위의 글에서 구성이 아닌 질감의 정보를 가지고 있다는 것은 눈, 코, 입 등에 대한 위치 정보가 아니라 눈, 코, 입에 대한 표현(패턴, 질감) 정보를 담고 있다는 것을 의미한다.

// 이미지

> 각 이미지들은 VGG 네트워크의 `conv1_1` (a),
`conv1_1` ,`conv2_1` (b), `conv1_1` ,`conv2_1`, `conv3_2` (c), `conv1_1` ,`conv2_1`, `conv3_2`, `conv4_2` (d) 그리고 `conv1_1` ,`conv2_1`, `conv3_2`, `conv4_2`, `conv5_2` (e) 레이어들로부터 얻었다.

즉, 네트워크의 서로 다른 레이어에 있는 style feature spaces로 정보를 캡쳐해, 입력 이미지의 스타일을 표현할 수 있다. 시각화는 white noise 이미지에 원본 이미지와의 gram matrix의 MSE를  gradient descent로 최소화하여 제작한다. 

원본 이미지를 $\vec{a}$, 생성된 이미지를 $\vec{x}$라고 하고, 그에 대응되는 레이어 l 스타일 표현을 $A^l$, $G^l$하고 하자. 레이어 l의 총 손실에 대한 기여도는 아래와 같다.

$$
E_l = \frac{1}{4N_l^2M_l^2} \sum_{i,j} (G_{ij}^l - A_{ij}^l)^2
$$

따라서 총 손실은 아래와 같다. $w_l$은 각 레이어가 총 손실에 기여하는 정도를 조정하는 가중치이다.

$$
L_{style}(\vec{a}, \vec{x}) = \sum_{l=0}^L w_lE_l
$$

그리고 레이어의 activation에 대한 $E^l$ 미분값은 아래와 같이 계산할 수 있다. 픽셀값 $\vec{x}$에 대한 $E^l$의 미분은 에러 역전파를 통해서 계산할 수 있다.

$$
\begin{align*}
\frac{\partial E_l}{\partial F_{ij}^l} = 
\begin{cases}
\frac{1}{N_l^2 M_l^2} ((F^l)^T (G^l-A^l))_{ji} &\text{if}\;F_{ij}^l > 0 \\
0 &\text{if}\;F_{ij}^l < 0 
\end{cases}
\end{align*}
$$

// 이미지2

### 2.3 Style transfer
예술품 $\vec{a}$의 스타일을 이미지 $\vec{p}$에 전달하기 위해서는 $\vec{p}$의 content representation과 $\vec{a}$ style representation에 점차적으로 가까워지는 새로운 이미지를 합성해야 한다. 따라서 우리는 하나의 층으로 이루어진 content representation과 여러층으로 이루어진 style representation으로부터의 white noise 이미지와의 거리를 동시에 최소화한다. 따라서 우리가 최소화할 최종 손실함수는 아래와 같다. $\alpha$, $\beta$는 각각 content와 style representaion에 대한 가중치 요소이다.

$$
L_{total}(\vec{p}, \vec{a}, \vec{x}) = \alpha L_{content}(\vec{p}, \vec{x}) + \beta L_{style} (\vec{a}, \vec{x})
$$

픽셋 값 $\frac{\partial L_{total}}{\partial \vec{x}}$에 대한 gradient는 다양한 최적화 전략에 입력으로 사용될 수 있다. 우리는 이미지 합성에서 잘 동작하는 L-BFGS를 사용하였다. 이미지 정보를 서로 비교 가능한 크기로 추출하기 위해, 스타일을 추출할 이미지와 내용을 추출할 이미지의 사이즈를 동일하게 만든 후 사용하였다. 마지막으로 우리는 이미지 합성 결과를 image prior로 규제하지 않았다. 

> image prior?  
> 이미지 합성, 복원에 사용되는 개념으로, 이미지의 특징이나 구조에 대한 사전 지식(이미지에 대한 특정 패턴이나 텍스처에 대한 규칙)을 의미한다. 이를 사용하면, 생성된 이미지를 더 자연스러운 이미지로 처리할 수 있다.  

하지만 네트워크의 낮은 층에서 추출한 텍스처 특징들이 스타일 이미지에 대한 image prior로 역할을 한다는 주장이 있을 수도 있다. 또한, 사용한 네트워크의 구조와 최적화 알고리즘에서의 영향으로 이미지 합성에 대한 결과에 차이가 있을수도 있다.

## 논문 구현 후 학습 결과

<img src="docs/content.jpg" width="500"/>
<img src="docs/style.jpg" width="500"/>
<img src="docs/result.jpg" width="500"/>
