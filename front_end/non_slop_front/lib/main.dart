import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_slidable/flutter_slidable.dart';

void main() {
  runApp(const MealPrepApp());
}

class MealPrepApp extends StatelessWidget {
  const MealPrepApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meal Variety',
      theme: ThemeData(useMaterial3: true),
      home: const HomePage(),
    );
  }
}

// ---------------- Models ----------------

class Ingredient {
  final String item;
  final String quantity;
  final String unit;

  Ingredient({required this.item, required this.quantity, required this.unit});

  factory Ingredient.fromJson(Map<String, dynamic> json) {
    return Ingredient(
      item: json['item'] ?? '',
      quantity: json['quantity'] ?? '',
      unit: json['unit'] ?? '',
    );
  }
}

class EstimatedPrice {
  final String currency;
  final double total;

  EstimatedPrice({required this.currency, required this.total});

  factory EstimatedPrice.fromJson(Map<String, dynamic> json) {
    return EstimatedPrice(
      currency: (json['currency'] ?? 'CAD') as String,
      total: (json['total'] as num?)?.toDouble() ?? 0.0,
    );
  }
}

class Meal {
  final String id;
  final String name;
  final List<Ingredient> ingredients;
  final List<String> instructions;
  final EstimatedPrice estimatedPrice;

  Meal({
    required this.id,
    required this.name,
    required this.ingredients,
    required this.instructions,
    required this.estimatedPrice,
  });

  factory Meal.fromJson(Map<String, dynamic> json) {
    final ingredientsJson = (json['ingredients'] as List<dynamic>? ?? []);
    final instructionsJson = (json['instructions'] as List<dynamic>? ?? []);
    return Meal(
      id: (json['id'] ?? UniqueKey().toString()) as String,
      name: (json['name'] ?? '') as String,
      ingredients: ingredientsJson
          .map((e) => Ingredient.fromJson(e as Map<String, dynamic>))
          .toList(),
      instructions: instructionsJson.map((e) => e.toString()).toList(),
      estimatedPrice: EstimatedPrice.fromJson(
          (json['estimated_price'] as Map<String, dynamic>? ?? {})),
    );
  }
}

// ---------------- Data loader ----------------

Future<List<Meal>> loadMealsFromAssets() async {
  final jsonString = await rootBundle.loadString('assets/mock_meals.json');
  final decoded = jsonDecode(jsonString) as Map<String, dynamic>;
  final meals = (decoded['meals'] as List<dynamic>? ?? []);
  return meals.map((e) => Meal.fromJson(e as Map<String, dynamic>)).toList();
}

// ---------------- UI ----------------

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<Meal> _meals = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    final meals = await loadMealsFromAssets();
    setState(() {
      _meals = meals;
      _loading = false;
    });
  }

  void _deleteMeal(String id) {
    setState(() {
      _meals.removeWhere((m) => m.id == id);
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Meal deleted')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Meals'),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _meals.isEmpty
              ? const Center(child: Text('No meals yet.'))
              : ListView.separated(
                  padding: const EdgeInsets.all(12),
                  itemCount: _meals.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 10),
                  itemBuilder: (context, index) {
                    final meal = _meals[index];

                    return Slidable(
                      key: ValueKey(meal.id),
                      endActionPane: ActionPane(
                        motion: const DrawerMotion(),
                        extentRatio: 0.28,
                        children: [
                          SlidableAction(
                            onPressed: (_) => _deleteMeal(meal.id),
                            icon: Icons.delete,
                            label: 'Delete',
                            backgroundColor: Colors.red,
                            foregroundColor: Colors.white,
                          ),
                        ],
                      ),
                      child: MealCard(
                        meal: meal,
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => MealDetailPage(meal: meal),
                            ),
                          );
                        },
                      ),
                    );
                  },
                ),
    );
  }
}

class MealCard extends StatelessWidget {
  final Meal meal;
  final VoidCallback onTap;

  const MealCard({super.key, required this.meal, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final priceText =
        '${meal.estimatedPrice.currency} ${meal.estimatedPrice.total.toStringAsFixed(2)}';

    return Material(
      borderRadius: BorderRadius.circular(16),
      color: Theme.of(context).colorScheme.surface,
      elevation: 2,
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Row(
            children: [
              const Icon(Icons.restaurant_menu),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  meal.name,
                  style: Theme.of(context).textTheme.titleMedium,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 12),
              Text(
                priceText,
                style: Theme.of(context).textTheme.titleSmall,
              ),
              const SizedBox(width: 6),
              const Icon(Icons.chevron_right),
            ],
          ),
        ),
      ),
    );
  }
}

class MealDetailPage extends StatelessWidget {
  final Meal meal;

  const MealDetailPage({super.key, required this.meal});

  @override
  Widget build(BuildContext context) {
    final priceText =
        '${meal.estimatedPrice.currency} ${meal.estimatedPrice.total.toStringAsFixed(2)}';

    return Scaffold(
      appBar: AppBar(title: Text(meal.name)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: [
              const Icon(Icons.payments),
              const SizedBox(width: 8),
              Text(
                'Estimated Price: $priceText',
                style: Theme.of(context).textTheme.titleMedium,
              ),
            ],
          ),
          const SizedBox(height: 18),

          Text('Ingredients',
              style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          ...meal.ingredients.map((ing) => Card(
                child: ListTile(
                  title: Text(ing.item),
                  subtitle: Text('${ing.quantity} ${ing.unit}'.trim()),
                  leading: const Icon(Icons.check_circle_outline),
                ),
              )),

          const SizedBox(height: 18),
          Text('Instructions',
              style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          ...List.generate(meal.instructions.length, (i) {
            return Card(
              child: ListTile(
                leading: CircleAvatar(child: Text('${i + 1}')),
                title: Text(meal.instructions[i]),
              ),
            );
          }),
        ],
      ),
    );
  }
}
