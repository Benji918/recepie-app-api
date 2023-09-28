"""Views for the recipe APIs"""

from core.models import Recipe, Tag, Ingredient
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import RecipeSerializer, RecipeDetailSerializer, TagSerializer, IngredientsSerializer, \
    RecipeImageSerializer


# Create your views here.
class RecipeViewSets(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated users only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe for a specific authenticated user"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class BaseRecipeAtrrViewSet(mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tags for only the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')


class TagViewSets(BaseRecipeAtrrViewSet):
    """ View manage recipe tags APIs"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSets(BaseRecipeAtrrViewSet):
    """ View manage recipe ingredients APIs"""
    serializer_class = IngredientsSerializer
    queryset = Ingredient.objects.all()
